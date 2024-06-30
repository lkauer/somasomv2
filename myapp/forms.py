from django import forms
from .models import Artista, Som
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nome', 'imagem_perfil']
        widgets = {
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_imagem_perfil(self):
        imagem_perfil = self.cleaned_data.get('imagem_perfil', False)
        if imagem_perfil:
            if not imagem_perfil.name.lower().endswith(('png', 'jpg', 'jpeg')):
                raise ValidationError("Apenas arquivos PNG e JPEG são permitidos.")
        return imagem_perfil

class SomForm(forms.ModelForm):
    class Meta:
        model = Som
        fields = ['titulo', 'artista', 'imagem_som', 'audio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SomForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['artista'].queryset = Artista.objects.filter(usuario=user)

    def clean_imagem_som(self):
        imagem_som = self.cleaned_data.get('imagem_som', False)
        if imagem_som:
            if not imagem_som.name.lower().endswith(('png', 'jpg', 'jpeg')):
                raise ValidationError("Apenas arquivos PNG e JPEG são permitidos.")
        return imagem_som

    def clean_audio(self):
        audio = self.cleaned_data.get('audio', False)
        if audio:
            if not audio.name.lower().endswith(('mp3', 'wav')):
                raise ValidationError("Apenas arquivos MP3 e WAV são permitidos.")
        return audio

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
