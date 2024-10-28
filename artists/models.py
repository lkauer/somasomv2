from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Artista(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem_perfil = models.ImageField(upload_to='artistas/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome