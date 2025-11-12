from django.db import models
from django.conf import settings
from user.models import User

class Group(models.Model):
    groupname = models.CharField(max_length=100)
    description = models.CharField(blank=True)
    created_by_UserId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='id',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.groupname

class Group_members(models.Model):
    ROLE_CHOICES = [
        ('LEADER', 'Leader'),
        ('MEMBER', 'Member'),
    ]

    GroupId = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='id',
    )
    UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='id',
    )
    role_in_group = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MEMBER',
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__ (self):
        return f"{self.user.username} in {self.group.groupname} ({self.role_in_group})"