from django import forms
from .models import Artista, Som
from django.core.exceptions import ValidationError

class SomForm(forms.ModelForm):
    class Meta:
        model = Som
        fields = ['titulo', 'artista', 'imagem_som', 'audio', 'descricao']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SomForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['artista'].queryset = Artista.objects.filter(usuario=user)
        self.fields['imagem_som'].label = 'Capa'

    def clean_imagem_som(self):
        imagem_som = self.cleaned_data.get('imagem_som', False)
        if imagem_som:
            if not imagem_som.name.lower().endswith(('png', 'jpg', 'jpeg')):
                raise ValidationError("Apenas arquivos PNG e JPEG são permitidos.")
        return imagem_som

    def clean_audio(self):
        audio = self.cleaned_data.get('audio', False)
        if audio:
            if not audio.name.lower().endswith(('mp3')):
                raise ValidationError("Apenas arquivos MP3 são permitidos.")
        return audio