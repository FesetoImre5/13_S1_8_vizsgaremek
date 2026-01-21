from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, IntegerField
from .models import User
from .serializers import UserSerializer, UserListSerializer, UserSearchSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'search':
            return UserSearchSerializer
        return UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).annotate(
            relevance=Case(
                When(email__iexact=query, then=Value(3)),
                When(email__icontains=query, then=Value(2)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('-relevance')[:10]

        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({"detail": "You can only edit your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({"detail": "You can only edit your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)