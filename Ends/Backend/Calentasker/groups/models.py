from django.db import models
from django.core.validators import URLValidator

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
    imageUrl = models.TextField(validators=[URLValidator()], blank=True, null=True)
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    active = models.BooleanField(default=True)
    parent_group = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subgroups')

    def __str__(self):
        return self.groupname

class GroupMember(models.Model):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('operator', 'Operator'),
        ('moderator', 'Moderator'),
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
        default='reader',
    )
    joined_at = models.DateTimeField(auto_now_add=True)