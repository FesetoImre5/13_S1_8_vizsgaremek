from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer, UserListSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]