from rest_framework import serializers
from .models import (
    Task, 
    Assigned, 
    Attachments, 
    Comment
)
from groups.models import Group
from users.serializers import UserListSerializer
from groups.serializers import GroupSerializer
from users.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        label = 'Posted by'
    )
    task = serializers.PrimaryKeyRelatedField(
        queryset = Task.objects.all(),
        write_only = True,
        label = 'Posted to'
    )
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, obj):
        from .serializers import TaskSerializer

        return TaskSerializer(obj.task).data
    
    user_detail = UserListSerializer(source = 'user', read_only = True)
    class Meta:
        model = Comment
        fields = (
            'id', 
            'task', 
            'task_detail',
            'user', 
            'user_detail',
            'content', 
            'created_at', 
            'active'
        )
        read_only_fields = ('created_at', 'user_detail', 'task_detail', 'active',)

class AttachmentsSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(
        queryset = Task.objects.all(),
        write_only = True,
        label = 'Attached to task'
    )
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, obj):
        from .serializers import TaskSerializer

        return TaskSerializer(obj.task).data

    uploaded_by_userid = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        label = 'Uploaded by',
    )
    uploaded_by_detail = UserListSerializer(source = 'uploaded_by_userid', read_only = True)

    class Meta:
        model = Attachments
        fields = (
            'id', 
            'task', 
            'task_detail',
            'uploaded_by_userid', 
            'uploaded_by_detail',
            'file', 
            'uploaded_at',
        )
        read_only_fields = ('uploaded_at', 'uploaded_by_detail', 'task_detail',)

class AssignedSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(
        queryset = Task.objects.all(),
        write_only = True,
        label = 'Assigned task',
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        label = 'Task assigned to',
    )
    task_detail = serializers.SerializerMethodField()

    def get_task_detail(self, obj):
        from .serializers import TaskSerializer

        return TaskSerializer(obj.task).data

    user_detail = UserListSerializer(source = 'user', read_only = True)
    class Meta:
        model = Assigned
        fields = (
            'id', 
            'task_detail',
            'user_detail',
            'task', 
            'user', 
            'assigned_at'
        )
        read_only_fields = ('task_detail', 'user_detail', 'assigned_at',) 

class TaskSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset = Group.objects.all(),
        write_only = True,
        label = 'in Group',
    )
    group_detail = GroupSerializer(source = 'group', read_only = True)
    created_by = UserListSerializer(source = 'created_by_userid', read_only = True)
    assigned_to = UserListSerializer(source = 'assigned_to_userid', read_only = True)
    assignments = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    comments = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    attachments = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'priority', 'status',
            'start_date', 'due_date', 'completed_at',
            'created_at', 'updated_at', 'active',
            'group', 'group_detail',
            'created_by',
            'assigned_to',
            'created_by_userid',
            'assigned_to_userid',
            'assignments', 'comments', 'attachments',
        )
        read_only_fields = ('group_detail', 'created_at', 'updated_at', 'completed_at', 'active',)
        extra_kwargs = {
            'created_by_userid': {'write_only': True},
            'assigned_to_userid': {'write_only': True},
        }