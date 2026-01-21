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
        # CHANGE: Removed .filter(active=True)
        # Now it fetches ALL tasks, even the "soft deleted" ones.
        queryset = Task.objects.select_related(
            'group', 
            'created_by_userid', 
            'assigned_to_userid'
        ).order_by('id')

        # Filters
        group_id = self.request.query_params.get('group')
        status = self.request.query_params.get('status')
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def perform_destroy(self, instance):
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
        queryset = Comment.objects.filter(active=True).order_by('created_at')
        task_id = self.request.query_params.get('task')
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        return queryset



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