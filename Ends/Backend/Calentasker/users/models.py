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
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_picture_url = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.username:
            # Generate username from first and last name
            base_username = f"{self.first_name}_{self.last_name}".strip()
            # Fallback if names are empty? User request specifically asked for first and last names.
            # If both are empty, base_username will be "_" or "", causing validation error if empty.
            # Assuming first/last are present as per request context, but good to be same.
            if base_username and base_username != "_":
                 self.username = base_username
            
        super().save(*args, **kwargs)

    @property
    def display_username(self):
        if self.username:
            return self.username
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email

    def __str__(self):
        return self.display_username