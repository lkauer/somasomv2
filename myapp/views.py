from artists.models import Artista
from sounds.models import Som
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
# from django.conf import settings
# from django.http import HttpResponse

def index(request):
            # Paginação para artistas
    artista_list = Artista.objects.order_by('-id')[:4]
    paginator_artists = Paginator(artista_list, 4)  # Mostra 4 artistas por página
    artista_page = request.GET.get('artista_page')
    try:
        artistas = paginator_artists.page(artista_page)
    except PageNotAnInteger:
        artistas = paginator_artists.page(1)
    except EmptyPage:
        artistas = paginator_artists.page(paginator_artists.num_pages)

    # Paginação para sons
    som_list = Som.objects.order_by('-id')[:4]
    paginator_sounds = Paginator(som_list, 4)  # Mostra 4 sons por página
    som_page = request.GET.get('som_page')
    try:
        sons = paginator_sounds.page(som_page)
    except PageNotAnInteger:
        sons = paginator_sounds.page(1)
    except EmptyPage:
        sons = paginator_sounds.page(paginator_sounds.num_pages)

    return render(request, 'myapp/index.html', {'artistas': artistas, 'sons': sons})

def about(request):
    return render(request, 'myapp/about.html')

# def privacy_policy(request):
#     return render(request, 'myapp/privacy_policy.html')

@login_required(login_url='/')
def general_panel(request):
    # Paginação para artistas
    artista_list = Artista.objects.filter(usuario=request.user)
    paginator_artists = Paginator(artista_list, 4)  # Mostra 4 artistas por página
    artista_page = request.GET.get('artista_page')
    try:
        artistas = paginator_artists.page(artista_page)
    except PageNotAnInteger:
        artistas = paginator_artists.page(1)
    except EmptyPage:
        artistas = paginator_artists.page(paginator_artists.num_pages)

    # Paginação para sons
    som_list = Som.objects.filter(usuario=request.user)
    paginator_sounds = Paginator(som_list, 4)  # Mostra 4 sons por página
    som_page = request.GET.get('som_page')
    try:
        sons = paginator_sounds.page(som_page)
    except PageNotAnInteger:
        sons = paginator_sounds.page(1)
    except EmptyPage:
        sons = paginator_sounds.page(paginator_sounds.num_pages)

    return render(request, 'myapp/painel.html', {'artistas': artistas, 'sons': sons})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('general_panel')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

def search_results(request):
    
    query = request.GET.get('q')
    if query:
        artistas_list = Artista.objects.filter(nome__icontains=query)
        sons_list = Som.objects.filter(titulo__icontains=query)
    else:
        artistas_list = Artista.objects.none()
        sons_list = Som.objects.none()

    # Paginando artistas
    artista_paginator = Paginator(artistas_list, 4)  # Mostra 4 artistas por página
    artista_page = request.GET.get('artista_page')
    try:
        artistas = artista_paginator.page(artista_page)
    except PageNotAnInteger:
        artistas = artista_paginator.page(1)
    except EmptyPage:
        artistas = artista_paginator.page(artista_paginator.num_pages)

    # Paginando sons
    som_paginator = Paginator(sons_list, 4)  # Mostra 4 sons por página
    som_page = request.GET.get('som_page')
    try:
        sons = som_paginator.page(som_page)
    except PageNotAnInteger:
        sons = som_paginator.page(1)
    except EmptyPage:
        sons = som_paginator.page(som_paginator.num_pages)

    context = {
        'query': query,
        'artistas': artistas,
        'sons': sons,
    }
    return render(request, 'myapp/search_results.html', context)
