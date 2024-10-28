from .forms import ArtistaForm
from .models import Artista
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from sounds.models import Som
def artist(request, pk):
    try:
        artista = Artista.objects.get(pk=pk)
        som_list = Som.objects.filter(artista=artista)
        paginator = Paginator(som_list, 4)  # Mostra 4 sons por página

        page = request.GET.get('page')
        try:
            sons = paginator.page(page)
        except PageNotAnInteger:
            # Se a página não for um inteiro, mostra a primeira página
            sons = paginator.page(1)
        except EmptyPage:
            # Se a página estiver fora do intervalo, mostra a última página
            sons = paginator.page(paginator.num_pages)

    except Artista.DoesNotExist:
        return render(request, 'artists/not_found.html', {'mensagem': 'Artista não encontrado.'})

    return render(request, 'artists/artist.html', {'artista': artista, 'sons': sons})

@login_required(login_url='/')
def add_artist(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            artista = form.save(commit=False)
            artista.usuario = request.user  # Atribui o usuário logado ao artista
            artista.save()
            return redirect('general_panel')  # Redireciona após o sucesso
    else:
        form = ArtistaForm()

    return render(request, 'artists/add_artist.html', {'form': form})

def list_artists(request):
    artista_list = Artista.objects.all()
    paginator = Paginator(artista_list, 8)  # Mostra 4 artistas por página

    page = request.GET.get('page')
    try:
        artistas = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        artistas = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        artistas = paginator.page(paginator.num_pages)

    return render(request, 'artists/list_artists.html', {'artistas': artistas})

@login_required(login_url='/')
def edit_artist(request, pk):
    try:
        artista = Artista.objects.get(pk=pk, usuario=request.user)
    except Artista.DoesNotExist:
        return render(request, 'artists/not_found.html', {'mensagem': 'Artista não encontrado.'})

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
            return redirect('general_panel')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'artists/edit_artist.html', {'form': form})

@login_required(login_url='/')
def delete_artist(request, pk):
    try:
        artista = Artista.objects.get(pk=pk, usuario=request.user)
    except Artista.DoesNotExist:
        return render(request, 'artists/not_found.html', {'mensagem': 'Artista não encontrado.'})

    if request.method == 'POST':
        # Remove o arquivo de imagem do servidor se existir
        if artista.imagem_perfil:
            if os.path.isfile(artista.imagem_perfil.path):
                os.remove(artista.imagem_perfil.path)

        artista.delete()
        return redirect('general_panel')

    return render(request, 'artists/confirm_artist_exclusion.html', {'artista': artista})