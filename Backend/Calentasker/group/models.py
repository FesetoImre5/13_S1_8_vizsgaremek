from django.db import models
from user.models import User

class Group(models.Model):
    groupname = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by_UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_created_UserId',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.groupname

class Group_members(models.Model):
    ROLE_CHOICES = [
        ('LEADER', 'Leader'),
        ('MEMBER', 'Member'),
    ]

    groupid = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group_member_GroupId',
    )
    userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_member_UserId',
    )
    role_in_group = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MEMBER',
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('groupid', 'userid')

    def __str__ (self):
        return f"{self.user.username} in {self.group.groupname} ({self.role_in_group})"