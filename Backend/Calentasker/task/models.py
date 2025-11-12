from django.db import models
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

    groupid = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='task_GroupId',
    )
    created_by_userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_created_UserId',
    )
    assigned_to_userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='task_assigned_UserId',
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
    taskid = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comment_TaskId',
    )
    userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_UserId',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.UserId.username} on {self-TaskId.title}"

class Assigned(models.Model):
    taskid = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assigned_TaskId',
    )
    userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_UserId',
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('taskid', 'userid')

    def __str__(self):
        return f"{self.UserId.username} assigned to {self.TaskId.title}"

class Attachment(models.Model):
    taskid = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachment_TaskId',
    )
    uploaded_by_userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attachment_UserId',  
    )
    file_path = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.TaskId.title} uploaded by {self.uploaded_by_UserId.username}"