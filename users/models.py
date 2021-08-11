from django.db import models
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('user', 'user'),
    )
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.TextField(max_length=100, blank=True)
    role = models.TextField(null=True, blank=True, choices=ROLES,
                            default='user')
