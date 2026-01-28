from rest_framework import serializers
from .models import Group, GroupMember
from users.serializers import UserListSerializer
from users.models import User

class GroupSerializer(serializers.ModelSerializer):
    created_by = UserListSerializer(source = 'created_by_userid',read_only = True)
    class Meta:
        model = Group
        fields = (
            'id', 
            'groupname', 
            'description',
            'created_by',
            'created_by_userid', 
            'created_at', 
            'active',
            'imageUrl',
        )
        read_only_fields = ('created_at', 'active',)
        extra_kwargs = {
            'created_by_userid': {'write_only': True},
        }

class GroupMemberSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset = Group.objects.all(),
        write_only = True,
        label = 'Member of group',
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        label = 'User'
    )
    group_detail = GroupSerializer(source = 'group', read_only = True)
    user_detail = UserListSerializer(source = 'user', read_only = True)

    class Meta:
        model = GroupMember
        fields = ('id', 'user_detail', 'group_detail', 'user', 'group', 'role', 'joined_at')
        read_only_fields = ('joined_at', 'group_detail', 'user_detail',)