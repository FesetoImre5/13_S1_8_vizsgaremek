from rest_framework import serializers
from .models import Group, GroupMember
from users.serializers import UserListSerializer

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only = True)
    class Meta:
        model = GroupMember
        fields = ('id', 'user', 'role', 'joined_at')
        read_only_fields = ('joined_at',)

class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True, read_only=True)
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
            'members',
        )
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'created_by_userid': {'write_only': True},
        }