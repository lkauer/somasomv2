# myapp/views.py
from .forms import ArtistaForm, LancamentoForm
from .models import Artista, Lancamento
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/')
def cadastrar_artista(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user  # Atribui o usuário logado ao artista
            artista.save()
            messages.success(request, 'Artista cadastrado com sucesso.')
            return redirect('listar_artistas')  # Redireciona após o sucesso
    else:
        form = ArtistaForm()

    return render(request, 'myapp/cadastrar_artista.html', {'form': form})

@login_required(login_url='/')
def editar_artista(request, pk):
    artista = get_object_or_404(Artista, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES, instance=artista)  # Adicione request.FILES aqui
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user
            artista.save()
            messages.success(request, 'Alteração realizada com sucesso.')
            return redirect('painel_geral')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'myapp/editar_artista.html', {'form': form})

@login_required(login_url='/')
def editar_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = LancamentoForm(request.POST, request.FILES, instance=lancamento)  # Adicione request.FILES aqui
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.usuario = request.user
            lancamento.save()
            messages.success(request, 'Alteração realizada com sucesso.')
            return redirect('painel_geral')
    else:
        form = LancamentoForm(instance=lancamento)
    return render(request, 'myapp/editar_lancamento.html', {'form': form})

@login_required(login_url='/')
def excluir_artista(request, pk):
    artista = get_object_or_404(Artista, pk=pk, usuario=request.user)
    if request.method == 'POST':
        artista.delete()
        return redirect('painel_geral')
    return render(request, 'myapp/confirmar_exclusao.html', {'artista': artista})

@login_required(login_url='/')
def excluir_lancamento(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk, usuario=request.user)
    if request.method == 'POST':
        lancamento.delete()
        return redirect('painel_geral')
    return render(request, 'myapp/confirmar_exclusao_lancamento.html', {'lancamento': lancamento})

def listar_artistas(request):
    artistas = Artista.objects.all()
    return render(request, 'myapp/listar_artistas.html', {'artistas': artistas})

@login_required(login_url='/')
def cadastrar_lancamento(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.usuario = request.user
            lancamento.save()
            messages.success(request, 'Lancamento cadastrado com sucesso.')
            return redirect('listar_lancamentos')
    else:
        form = LancamentoForm(user=request.user)

    return render(request, 'myapp/cadastrar_lancamento.html', {'form': form})


def listar_lancamentos(request):
    lancamentos = Lancamento.objects.all()
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

def index(request):
    return render(request, 'myapp/index.html')

@login_required(login_url='/')
def painel_geral(request):
    artistas = Artista.objects.filter(usuario=request.user)
    lancamentos = Lancamento.objects.filter(usuario=request.user)

    return render(request, 'myapp/painel.html', {'artistas': artistas, 'lancamentos': lancamentos})