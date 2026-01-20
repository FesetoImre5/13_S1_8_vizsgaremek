from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'display_name', 'profile_picture', 'first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined')
        read_only_fields = ('is_active', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'display_name', 'profile_picture', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = fields