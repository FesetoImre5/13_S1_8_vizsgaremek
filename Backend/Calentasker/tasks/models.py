from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    STATUS_CHOICES =(
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('archived', 'Archived'),
    )

    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.SET_NULL,
        null=True,
        blank = True,
        related_name='tasks',
    )
    created_by_userid = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
    )
    assigned_to_userid = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='low'
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='todo'
    )
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Assigned(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

class Attachments(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    uploaded_by_userid = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)