from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    display_username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture', 'first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined')
        read_only_fields = ('is_active', 'date_joined', 'display_username')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSearchSerializer(serializers.ModelSerializer):
    display_username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'display_username', 'first_name', 'last_name', 'profile_picture')

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'display_username', 'profile_picture', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = fields