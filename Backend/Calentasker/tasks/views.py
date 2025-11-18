from rest_framework import viewsets
from .models import Task, Assigned, Attachments, Comment
from .serializers import (
    TaskSerializer, 
    AssignedSerializer, 
    AttachmentsSerializer, 
    CommentSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(active=True).order_by('-created_at')
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = self.queryset
        group_id = self.request.query_params.get('group')
        status = self.request.query_params.get('status')
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class AssignedViewSet(viewsets.ModelViewSet):
    queryset = Assigned.objects.all()
    serializer_class = AssignedSerializer

class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by_userid=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True).order_by('created_at')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)