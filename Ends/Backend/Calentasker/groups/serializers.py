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
            'image',
            'parent_group',
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
        label = 'User',
        required = False,
    )
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    group_detail = GroupSerializer(source = 'group', read_only = True)
    user_detail = UserListSerializer(source = 'user', read_only = True)

    class Meta:
        model = GroupMember
        fields = ('id', 'user_detail', 'group_detail', 'user', 'group', 'username', 'email', 'role', 'joined_at')
        read_only_fields = ('joined_at', 'group_detail', 'user_detail',)
    
    def create(self, validated_data):
        # Priority: user (already in validated_data if ID passed) > email > username
        user = validated_data.get('user')
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)

        if not user:
            if email:
                try:
                    user = User.objects.get(email__iexact=email)
                    validated_data['user'] = user
                except User.DoesNotExist:
                    raise serializers.ValidationError({'email': 'User with this email does not exist.'})
            elif username:
                try:
                    user = User.objects.get(username__iexact=username)
                    validated_data['user'] = user
                except User.DoesNotExist:
                    raise serializers.ValidationError({'username': 'User with this username does not exist.'})
            else:
                 raise serializers.ValidationError({'detail': 'Must provide user ID, email, or username.'})

        # Check if user is already a member of this group
        if GroupMember.objects.filter(group=validated_data['group'], user=validated_data['user']).exists():
            raise serializers.ValidationError({'detail': 'User is already a member of this group.'})
        
        return super().create(validated_data)