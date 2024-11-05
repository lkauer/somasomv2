from .forms import TopicForm, TopicPostForm
from .models import Topic, TopicPost
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/')
def index(request):
    
    topic_list = Topic.objects.all()
    paginator = Paginator(topic_list, 8)  # Mostra 8 sons por página

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, mostra a primeira página
        topics = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostra a última página
        topics = paginator.page(paginator.num_pages)

    return render(request, 'community/index.html', {'topics': topics})

@login_required(login_url='/')
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect('/community')  # Redireciona após o sucesso
    else:
        form = TopicForm()

    return render(request, 'community/add_topic.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='/')
def topic(request, pk):
    topic = Topic.objects.get(pk=pk)
    topic_posts = TopicPost.objects.filter(topic=topic)
    form = TopicPostForm()

    paginator = Paginator(topic_posts, 10)
    page = request.GET.get('page')
    try:
        topic_posts = paginator.page(page)
    except PageNotAnInteger:
        topic_posts = paginator.page(1)
    except EmptyPage:
        topic_posts = paginator.page(paginator.num_pages)

    return render(request, 'community/topic.html', {'topic': topic, 'topic_posts': topic_posts, 'form':form})

@login_required(login_url='/')
def edit_topic(request, pk):
    try:
        topic = Topic.objects.get(pk=pk, user=request.user)
    except Topic.DoesNotExist:
        return render(request, 'community/not_found.html', {'mensagem': 'Topico não encontrado.'})

    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user

            topic.save()
            return redirect('general_panel')
    else:
        form = TopicForm(instance=topic)
    return render(request, 'community/edit_topic.html', {'form': form})

@login_required(login_url='/')
def delete_topic(request, pk):
    try:
        topic = Topic.objects.get(pk=pk, user=request.user)
    except Topic.DoesNotExist:
        return render(request, 'community/not_found.html', {'mensagem': 'Topico não encontrado.'})

    if request.method == 'POST':
        topic.delete()
        return redirect('general_panel')

    return render(request, 'community/confirm_topic_exclusion.html', {'topic': topic})

@login_required(login_url='/')
def add_post_topic(request, pk):
    topic = Topic.objects.get(pk=pk)
    if request.method == 'POST':
        form = TopicPostForm(request.POST)
        print("Form data:", request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.user = request.user
            post.save()
            return redirect('community:topic', pk=pk)
    else:
        form = TopicPostForm()
    return render(request, 'community/topic.html', {'form': form, 'topic': topic})


@login_required(login_url='/')
def delete_post_topic(request, pk):
    post = get_object_or_404(TopicPost, pk=pk)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post excluído com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para excluir este post.")
    return redirect('community:topic', pk=post.topic.pk)
