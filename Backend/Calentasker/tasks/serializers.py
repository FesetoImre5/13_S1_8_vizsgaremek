from rest_framework import serializers
from .models import (
    Task, 
    Assigned, 
    Attachments, 
    Comment
)
from users.serializers import UserListSerializer
from groups.serializers import GroupSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = ('id', 'task', 'user', 'content', 'created_at', 'active')
        read_only_fields = ('created_at', 'task',)

class AttachmentsSerializer(serializers.ModelSerializer):
    uploaded_by = UserListSerializer(source = 'uploaded_by_userid', read_only = True)
    class Meta:
        model = Attachments
        fields = ('id', 'task', 'uploaded_by', 'file', 'uploaded_at')
        read_only_fields = ('uploaded_at', 'task',)

class AssignedSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only = True)
    class Meta:
        model = Assigned
        fields = ('id', 'user', 'assigned_at')
        read_only_fields = ('assigned_at',) 

class TaskSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    created_by = UserListSerializer(source = 'created_by_userid', read_only = True)
    assigned_to = UserListSerializer(source = 'assigned_to_userid', read_only = True)
    assignments = AssignedSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentsSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'priority', 'status',
            'start_date', 'due_date', 'completed_at',
            'created_at', 'updated_at', 'active',
            'group',
            'created_by',
            'assigned_to',
            'created_by_userid',
            'assigned_to_userid',
            'assignments', 'comments', 'attachments',
        )
        read_only_fields = ('created_at', 'updated_at',)
        extra_kwargs = {
            'created_by_userid': {'write_only': True},
            'assigned_to_userid': {'write_only': True},
        }