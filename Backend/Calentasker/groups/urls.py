from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GroupViewSet, GroupMemberViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'group-members', GroupMemberViewSet, basename='group-member')

urlpatterns = [
    path('', include(router.urls))
]