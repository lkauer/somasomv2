from .forms import ArtistaForm, SomForm
from .models import Artista, Som
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings

def index(request):
    return render(request, 'myapp/index.html')

def visualizar_som(request, pk):
    try:
        som = Som.objects.get(pk=pk)
    except Som.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Som não encontrado.'})

    return render(request, 'myapp/visualizar_som.html', {'som': som})

def visualizar_artista(request, pk):
    try:
        artista = Artista.objects.get(pk=pk)
        sons = Som.objects.filter(artista=artista)
    except Artista.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Artista não encontrado.'})

    return render(request, 'myapp/visualizar_artista.html', {'artista': artista, 'sons': sons})

@login_required(login_url='/')
def painel_geral(request):
    artistas = Artista.objects.filter(usuario=request.user)
    sons = Som.objects.filter(usuario=request.user)

    return render(request, 'myapp/painel.html', {'artistas': artistas, 'sons': sons})

@login_required(login_url='/')
def cadastrar_artista(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user  # Atribui o usuário logado ao artista
            artista.save()
            return redirect('painel_geral')  # Redireciona após o sucesso
    else:
        form = ArtistaForm()

    return render(request, 'myapp/cadastrar_artista.html', {'form': form})

@login_required(login_url='/')
def cadastrar_som(request):
    if request.method == 'POST':
        form = SomForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            som = form.save(commit=False)
            som.usuario = request.user
            som.save()
            return redirect('painel_geral')
    else:
        form = SomForm(user=request.user)

    return render(request, 'myapp/cadastrar_som.html', {'form': form})

def listar_artistas(request):
    artista_list = Artista.objects.all()
    paginator = Paginator(artista_list, 5)  # Mostra 5 artistas por página

    page = request.GET.get('page')
    try:
        artistas = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        artistas = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        artistas = paginator.page(paginator.num_pages)

    return render(request, 'myapp/listar_artistas.html', {'artistas': artistas})

def listar_sons(request):
    som_list = Som.objects.all()
    paginator = Paginator(som_list, 5)  # Mostra 5 sons por página

    page = request.GET.get('page')
    try:
        sons = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        sons = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        sons = paginator.page(paginator.num_pages)

    return render(request, 'myapp/listar_sons.html', {'sons': sons})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('painel_geral')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

@login_required(login_url='/')
def editar_artista(request, pk):
    try:
        artista = Artista.objects.get(pk=pk, usuario=request.user)
    except Artista.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Artista não encontrado.'})

    imagem_anterior = artista.imagem_perfil.path if artista.imagem_perfil else None  # Armazena o caminho da imagem anterior

    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES, instance=artista)
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user

            # Verifica se o campo de imagem foi limpo
            if 'imagem_perfil-clear' in request.POST and imagem_anterior:
                if os.path.isfile(imagem_anterior):
                    os.remove(imagem_anterior)
                artista.imagem_perfil = None

            artista.save()
            return redirect('painel_geral')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'myapp/editar_artista.html', {'form': form})

@login_required(login_url='/')
def editar_som(request, pk):
    try:
        som = Som.objects.get(pk=pk, usuario=request.user)
    except Som.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Som não encontrado.'})

    imagem_anterior = som.imagem_som.path if som.imagem_som else None  # Armazena o caminho da imagem anterior
    audio_anterior = som.audio.path if som.audio else None  # Armazena o caminho do áudio anterior

    if request.method == 'POST':
        form = SomForm(request.POST, request.FILES, instance=som, user=request.user)
        if form.is_valid():
            som = form.save(commit=False)
            som.usuario = request.user

            # Verifica se o campo de imagem foi limpo
            if 'imagem_som-clear' in request.POST and imagem_anterior:
                if os.path.isfile(imagem_anterior):
                    os.remove(imagem_anterior)
                som.imagem_som = None

            # Verifica se o campo de áudio foi limpo
            if 'audio-clear' in request.POST and audio_anterior:
                if os.path.isfile(audio_anterior):
                    os.remove(audio_anterior)
                som.audio = None

            som.save()
            return redirect('painel_geral')
    else:
        form = SomForm(instance=som, user=request.user)
    return render(request, 'myapp/editar_som.html', {'form': form})

@login_required(login_url='/')
def excluir_artista(request, pk):
    try:
        artista = Artista.objects.get(pk=pk, usuario=request.user)
    except Artista.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Artista não encontrado.'})

    if request.method == 'POST':
        # Remove o arquivo de imagem do servidor se existir
        if artista.imagem_perfil:
            if os.path.isfile(artista.imagem_perfil.path):
                os.remove(artista.imagem_perfil.path)

        artista.delete()
        return redirect('painel_geral')

    return render(request, 'myapp/confirmar_exclusao.html', {'artista': artista})

@login_required(login_url='/')
def excluir_som(request, pk):
    try:
        som = Som.objects.get(pk=pk, usuario=request.user)
    except Som.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Som não encontrado.'})

    if request.method == 'POST':
        # Remove o arquivo de imagem do servidor se existir
        if som.imagem_som:
            if os.path.isfile(som.imagem_som.path):
                os.remove(som.imagem_som.path)

        # Remove o arquivo de áudio do servidor se existir
        if som.audio:
            if os.path.isfile(som.audio.path):
                os.remove(som.audio.path)

        som.delete()
        return redirect('painel_geral')

    return render(request, 'myapp/confirmar_exclusao_som.html', {'som': som})
