from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(active=True).order_by('groupname')
    serializer_class = GroupSerializer
class GroupMemberViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = GroupMember.objects.all().order_by('group__groupname')
    serializer_class = GroupMemberSerializer

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group')
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
        return queryset