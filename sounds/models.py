from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from artists.models import Artista

User = get_user_model()

class Som(models.Model):
    titulo = models.CharField(max_length=200)
    imagem_som = models.ImageField(upload_to='sons/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])], blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo
