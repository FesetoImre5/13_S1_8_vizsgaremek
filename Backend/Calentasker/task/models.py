from django.db import models
from django.conf import settings
from group.models import Group
from user.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('TO_DO', 'To do'),
        ('IN_PROGRESS', 'In progress'),
        ('DONE', 'Done'),
        ('ARCHIVED', 'Archived'),
    ]

    GroupId = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='id',
    )
    created_by_UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='id',
    )
    assigned_to_UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='id',
    )
    title = models.CharField(max_length=150)
    description = models.CharField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='LOW',
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TO_DO',
    )
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    TaskId = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='id',
    )
    UserId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='id',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.UserId.username} on {self-TaskId.title}"

class Assigned(models.Model):
    TaskId = models.IntegerField()
    UserId = models.IntegerField()
    assigned_at = models.DateTimeField()

class Attachment(models.Model):
    TaskId = models.IntegerField()
    uploaded_by_UserId = models.IntegerField()
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField()