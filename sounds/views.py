from .forms import SomForm
from .models import Som
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

def sound(request, pk):
    try:
        som = Som.objects.get(pk=pk)
    except Som.DoesNotExist:
        return render(request, 'sounds/not_found.html', {'mensagem': 'Som não encontrado.'})

    return render(request, 'sounds/sound.html', {'som': som})


@login_required(login_url='/')
def add_sound(request):
    if request.method == 'POST':
        form = SomForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            som = form.save(commit=False)
            som.usuario = request.user
            som.save()
            return redirect('general_panel')
    else:
        form = SomForm(user=request.user)

    return render(request, 'sounds/add_sound.html', {'form': form})


def list_sounds(request):
    som_list = Som.objects.all()
    paginator = Paginator(som_list, 8)  # Mostra 8 sons por página

    page = request.GET.get('page')
    try:
        sons = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        sons = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        sons = paginator.page(paginator.num_pages)

    return render(request, 'sounds/list_sounds.html', {'sons': sons})

@login_required(login_url='/')
def edit_sound(request, pk):
    try:
        som = Som.objects.get(pk=pk, usuario=request.user)
    except Som.DoesNotExist:
        return render(request, 'sounds/not_found.html', {'mensagem': 'Som não encontrado.'})

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
            return redirect('general_panel')
    else:
        form = SomForm(instance=som, user=request.user)
    return render(request, 'sounds/edit_sound.html', {'form': form})

@login_required(login_url='/')
def delete_sound(request, pk):
    try:
        som = Som.objects.get(pk=pk, usuario=request.user)
    except Som.DoesNotExist:
        return render(request, 'sounds/not_found.html', {'mensagem': 'Som não encontrado.'})

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
        return redirect('general_panel')

    return render(request, 'sounds/confirm_sound_exclusion.html', {'som': som})