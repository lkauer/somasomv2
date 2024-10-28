from django import forms
from .models import Artista
from django.core.exceptions import ValidationError

class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nome', 'imagem_perfil', 'descricao']
        widgets = {
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_imagem_perfil(self):
        imagem_perfil = self.cleaned_data.get('imagem_perfil', False)
        if imagem_perfil:
            if not imagem_perfil.name.lower().endswith(('png', 'jpg', 'jpeg')):
                raise ValidationError("Apenas arquivos PNG e JPEG são permitidos.")
        return imagem_perfil