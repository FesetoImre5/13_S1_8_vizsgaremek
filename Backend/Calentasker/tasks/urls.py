from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TaskViewSet, 
    AssignedViewSet, 
    AttachmentsViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'assignments', AssignedViewSet, basename='assignments')
router.register(r'attachments', AttachmentsViewSet, basename='attachment')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns =[
    path('', include(router.urls))
]