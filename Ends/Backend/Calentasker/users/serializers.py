from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'display_username', 'profile_picture', 'profile_picture_url', 'first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined')
        read_only_fields = ('is_active', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'display_username', 'first_name', 'last_name', 'profile_picture')

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'display_username', 'profile_picture', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = fields