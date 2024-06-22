from django import forms
from .models import Artista, Lancamento
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nome', 'imagem_perfil']
        widgets = {
            'imagem_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['titulo', 'artista', 'data_lancamento', 'imagem_lancamento', 'audio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LancamentoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['artista'].queryset = Artista.objects.filter(usuario=user)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
