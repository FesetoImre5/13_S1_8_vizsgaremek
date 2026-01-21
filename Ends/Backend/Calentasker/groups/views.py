from rest_framework import viewsets, mixins
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

class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group')
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
        return queryset