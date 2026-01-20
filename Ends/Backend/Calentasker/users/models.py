from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', # <-- FIX 1: Unique related_name for AUTH groups
        blank=True,
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # <-- FIX 2: Unique related_name for AUTH permissions
        blank=True,
        verbose_name=('user permissions'),
    )
    display_name = models.CharField(max_length=150, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)