from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Task, Assigned, Attachments, Comment
from .serializers import (
    TaskSerializer, 
    AssignedSerializer, 
    AttachmentsSerializer, 
    CommentSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # CHANGE: Restored active=True to filter out soft-deleted tasks
        queryset = Task.objects.select_related(
            'group', 
            'created_by_userid', 
            'assigned_to_userid'
        ).filter(active=True).order_by('id')

        # Filters
        group_id = self.request.query_params.get('group')
        status = self.request.query_params.get('status')
        created_by_userid = self.request.query_params.get('created_by_userid')
        group_isnull = self.request.query_params.get('group__isnull')
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if status:
            queryset = queryset.filter(status=status)
        if created_by_userid:
            queryset = queryset.filter(created_by_userid=created_by_userid)
        if group_isnull:
            # If 'true' or 'True', filter for null group
            if group_isnull.lower() == 'true':
                queryset = queryset.filter(group__isnull=True)
        
        # Ensure we don't show tasks from deleted groups
        # We perform this check for tasks that HAVE a group.
        # Since we use select_related('group'), we can filter generally on group__active.
        # Tasks with group=None (Own Tasks) have group__active as Null/None, so we need Q objects.
        
        from django.db.models import Q
        queryset = queryset.filter(Q(group__isnull=True) | Q(group__active=True))
            
        return queryset

    def perform_create(self, serializer):
        group = serializer.validated_data.get('group')
        created_by = serializer.validated_data.get('created_by_userid')

        # If no group specified, allow creation (or handle as per requirement, assumed allowed for personal if supported)
        if group and created_by:
            from groups.models import GroupMember
            from rest_framework.exceptions import PermissionDenied
            
            try:
                membership = GroupMember.objects.get(group=group, user=created_by)
                # Check Role
                if membership.role not in ['leader', 'operator']:
                    raise PermissionDenied("Only Leaders and Operators can create tasks for this server.")
            except GroupMember.DoesNotExist:
                 raise PermissionDenied("You are not a member of this server.")

        serializer.save()

    def perform_destroy(self, instance):
        from groups.models import GroupMember
        from rest_framework.exceptions import PermissionDenied

        user = self.request.user
        
        if instance.group:
            # Group Task: Only Leader or Operator
            try:
                member = GroupMember.objects.get(group=instance.group, user=user)
                if member.role not in ['leader', 'operator']:
                     raise PermissionDenied("Only Leaders and Operators can delete tasks in this group.")
            except GroupMember.DoesNotExist:
                raise PermissionDenied("You are not a member of this group.")
        else:
            # Own Task: Only Creator
            if instance.created_by_userid != user:
                raise PermissionDenied("You can only delete your own personal tasks.")

        instance.active = False
        instance.save()

class AssignedViewSet(viewsets.ModelViewSet):
    queryset = Assigned.objects.all()
    serializer_class = AssignedSerializer

class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(active=True).order_by('-created_at')
        task_id = self.request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset

    def perform_update(self, serializer):
        from rest_framework.exceptions import PermissionDenied
        if self.request.user != serializer.instance.user:
             raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        from rest_framework.exceptions import PermissionDenied
        if self.request.user != instance.user:
             raise PermissionDenied("You can only delete your own comments.")
        
        instance.active = False
        instance.save()



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'display_username': user.display_username
        })