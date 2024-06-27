# myapp/views.py
from .forms import ArtistaForm, LancamentoForm
from .models import Artista, Lancamento
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.conf import settings

def index(request):
    return render(request, 'myapp/index.html')

def manifesto(request):

    return render(request, 'myapp/manifesto.html')

@login_required(login_url='/')
def visualizar_lancamento(request, pk):
    try:
        lancamento = Lancamento.objects.get(pk=pk)
    except Lancamento.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Lançamento não encontrado.'})

    return render(request, 'myapp/visualizar_lancamento.html', {'lancamento': lancamento})

def visualizar_artista(request, pk):

    try:
        artista = Artista.objects.get(pk=pk)
        lancamentos = Lancamento.objects.filter(artista=artista)
    except Artista.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Artista não encontrado.'})

    return render(request, 'myapp/visualizar_artista.html', {'artista': artista, 'lancamentos': lancamentos})

@login_required(login_url='/')
def painel_geral(request):

    artistas = Artista.objects.filter(usuario=request.user)
    lancamentos = Lancamento.objects.filter(usuario=request.user)

    return render(request, 'myapp/painel.html', {'artistas': artistas, 'lancamentos': lancamentos})

@login_required(login_url='/')
def cadastrar_artista(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user  # Atribui o usuário logado ao artista
            artista.save()
            messages.success(request, 'Artista cadastrado com sucesso.')
            return redirect('painel_geral')  # Redireciona após o sucesso
    else:
        form = ArtistaForm()

    return render(request, 'myapp/cadastrar_artista.html', {'form': form})

@login_required(login_url='/')
def cadastrar_lancamento(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.usuario = request.user
            lancamento.save()
            messages.success(request, 'Lancamento cadastrado com sucesso.')
            return redirect('painel_geral')
    else:
        form = LancamentoForm(user=request.user)

    return render(request, 'myapp/cadastrar_lancamento.html', {'form': form})

def listar_artistas(request):
    artista_list = Artista.objects.all()
    paginator = Paginator(artista_list, 10)  # Mostra 10 artistas por página

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

def listar_lancamentos(request):
    lancamento_list = Lancamento.objects.all()
    paginator = Paginator(lancamento_list, 10)  # Mostra 10 lançamentos por página

    page = request.GET.get('page')
    try:
        lancamentos = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        lancamentos = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        lancamentos = paginator.page(paginator.num_pages)

    return render(request, 'myapp/listar_lancamentos.html', {'lancamentos': lancamentos})

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
            messages.success(request, 'Alteração realizada com sucesso.')
            return redirect('painel_geral')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'myapp/editar_artista.html', {'form': form})

@login_required(login_url='/')
def editar_lancamento(request, pk):
    try:
        lancamento = Lancamento.objects.get(pk=pk, usuario=request.user)
    except Lancamento.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Lancamento não encontrado.'})

    imagem_anterior = lancamento.imagem_lancamento.path if lancamento.imagem_lancamento else None  # Armazena o caminho da imagem anterior
    audio_anterior = lancamento.audio.path if lancamento.audio else None  # Armazena o caminho do áudio anterior

    if request.method == 'POST':
        form = LancamentoForm(request.POST, request.FILES, instance=lancamento, user=request.user)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.usuario = request.user

            # Verifica se o campo de imagem foi limpo
            if 'imagem_lancamento-clear' in request.POST and imagem_anterior:
                if os.path.isfile(imagem_anterior):
                    os.remove(imagem_anterior)
                lancamento.imagem_lancamento = None

            # Verifica se o campo de áudio foi limpo
            if 'audio-clear' in request.POST and audio_anterior:
                if os.path.isfile(audio_anterior):
                    os.remove(audio_anterior)
                lancamento.audio = None

            lancamento.save()
            messages.success(request, 'Alteração realizada com sucesso.')
            return redirect('painel_geral')
    else:
        form = LancamentoForm(instance=lancamento, user=request.user)
    return render(request, 'myapp/editar_lancamento.html', {'form': form})

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
def excluir_lancamento(request, pk):
    try:
        lancamento = Lancamento.objects.get(pk=pk, usuario=request.user)
    except Lancamento.DoesNotExist:
        return render(request, 'myapp/registro_nao_encontrado.html', {'mensagem': 'Lançamento não encontrado.'})

    if request.method == 'POST':
        # Remove o arquivo de imagem do servidor se existir
        if lancamento.imagem_lancamento:
            if os.path.isfile(lancamento.imagem_lancamento.path):
                os.remove(lancamento.imagem_lancamento.path)

        # Remove o arquivo de áudio do servidor se existir
        if lancamento.audio:
            if os.path.isfile(lancamento.audio.path):
                os.remove(lancamento.audio.path)

        lancamento.delete()
        return redirect('painel_geral')

    return render(request, 'myapp/confirmar_exclusao_lancamento.html', {'lancamento': lancamento})