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

class Artista(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem_perfil = models.ImageField(upload_to='artistas/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Som(models.Model):
    titulo = models.CharField(max_length=200)
    imagem_som = models.ImageField(upload_to='sons/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])], blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo
