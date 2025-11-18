from django.db import models

class Group(models.Model):
    groupname = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by_userid = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_groups',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class GroupMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('leader', 'Leader'),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='members',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='member_groups',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='member',
    )
    joined_at = models.DateTimeField(auto_now_add=True)