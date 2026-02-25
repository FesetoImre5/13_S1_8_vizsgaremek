from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, IntegerField
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import User
from .serializers import UserSerializer, UserListSerializer, UserSearchSerializer

class UserViewSet(viewsets.ModelViewSet):
    # Only list active users
    queryset = User.objects.filter(is_active=True).order_by('id')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'search':
            return UserSearchSerializer
        return UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action in ['create', 'activate']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        # Save user as inactive initially
        user = serializer.save(is_active=False)
        
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build verification URL
        # Assuming frontend runs on localhost:5173 as per user context
        verification_url = f"http://localhost:5173/verify-email/{uid}/{token}"
        
        # Send email
        subject = 'Activate your Calentasker account'
        message = f'Hi {user.username},\n\nPlease click the link below to activate your account:\n\n{verification_url}\n\nThanks!'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

    @action(detail=False, methods=['post'])
    def activate(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        if not uid or not token:
            return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account successfully activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid confirmation link.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([], status=status.HTTP_200_OK)

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            is_active=True # Ensure search only returns active users
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({"detail": "You can only delete your own profile."}, status=status.HTTP_403_FORBIDDEN)
        
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
