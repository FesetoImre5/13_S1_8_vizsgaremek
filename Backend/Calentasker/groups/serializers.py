from rest_framework import serializers
from .models import Group, GroupMember
from users.serializers import UserListSerializer

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
        )
        read_only_fields = ('created_at', 'active',)
        extra_kwargs = {
            'created_by_userid': {'write_only': True},
        }

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserListSerializer(source = 'users.User', read_only = True)
    group = GroupSerializer(source = Group, read_only = True)
    class Meta:
        model = GroupMember
        fields = ('group', 'user', 'role', 'joined_at')
        read_only_fields = ('joined_at',)
        extra_kwargs = {
            'group' : {'write_only': True},
            'user' : {'write_only': True},
        }