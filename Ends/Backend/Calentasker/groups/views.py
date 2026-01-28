from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(active=True).order_by('groupname')
    serializer_class = GroupSerializer
    
    def get_queryset(self):
        queryset = Group.objects.filter(active=True).order_by('groupname')
        
        parent_group = self.request.query_params.get('parent_group')
        # Filter by parent_group if provided
        if parent_group is not None:
             queryset = queryset.filter(parent_group=parent_group)
        # If 'root' is requested, filter for top-level groups (no parent)
        elif self.request.query_params.get('root') == 'true':
             queryset = queryset.filter(parent_group__isnull=True)
             
        return queryset

    def perform_create(self, serializer):
        # Save group with the creator
        group = serializer.save(created_by_userid=self.request.user)
        
        # Add creator as a member (Leader)
        GroupMember.objects.create(
            group=group,
            user=self.request.user,
            role='leader'
        )

    def perform_destroy(self, instance):
        # Soft Delete + Permission Check
        user = self.request.user
        
        # Check if user is a Leader of this group
        try:
            member = GroupMember.objects.get(group=instance, user=user)
            if member.role != 'leader':
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Only Group Leaders can delete this group.")
        except GroupMember.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this group.")

        instance.active = False
        instance.active = False
        instance.save()

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        
        # Check if user is a Leader of this group
        try:
            from groups.models import GroupMember
            member = GroupMember.objects.get(group=instance, user=user)
            if member.role != 'leader':
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Only Group Leaders can edit this group.")
        except GroupMember.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a member of this group.")

        serializer.save()

    @action(detail=True, methods=['post'])
    def transfer_leadership(self, request, pk=None):
        group = self.get_object()
        user = request.user
        new_leader_id = request.data.get('new_leader_id')

        if not new_leader_id:
            return Response({'detail': 'new_leader_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Verify Request User is Leader
        try:
            current_leader_membership = GroupMember.objects.get(group=group, user=user)
            if current_leader_membership.role != 'leader':
                return Response({'detail': 'Only the group leader can transfer leadership.'}, status=status.HTTP_403_FORBIDDEN)
        except GroupMember.DoesNotExist:
             return Response({'detail': 'You are not a member of this group.'}, status=status.HTTP_403_FORBIDDEN)

        # 2. Verify New Leader is a Member
        try:
            new_leader_membership = GroupMember.objects.get(group=group, user_id=new_leader_id)
        except GroupMember.DoesNotExist:
            return Response({'detail': 'Target user is not a member of this group.'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Perform Swap
        current_leader_membership.role = 'reader' # Demote self
        new_leader_membership.role = 'leader'     # Promote other
        
        current_leader_membership.save()
        new_leader_membership.save()
        
        return Response({'detail': 'Leadership transferred successfully.'})

class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group')
        user_id = self.request.query_params.get('user')
        
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
            
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
            
        # Ensure we only return members of ACTIVE groups
        queryset = queryset.filter(group__active=True)
            
        return queryset