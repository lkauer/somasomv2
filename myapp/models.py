from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    # Adicionar related_name para evitar conflitos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Nome alternativo para evitar conflito
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions_set',  # Nome alternativo para evitar conflito
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

User = get_user_model()