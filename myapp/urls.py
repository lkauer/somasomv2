from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar_artista/', views.cadastrar_artista, name='cadastrar_artista'),
    path('editar_artista/<int:pk>/', views.editar_artista, name='editar_artista'),
    path('editar_lancamento/<int:pk>/', views.editar_lancamento, name='editar_lancamento'),
    path('excluir_artista/<int:pk>/', views.excluir_artista, name='excluir_artista'),
    path('excluir_lancamento/<int:pk>/', views.excluir_lancamento, name='excluir_lancamento'),
    path('listar_artistas/', views.listar_artistas, name='listar_artistas'),
    path('cadastrar_lancamento/', views.cadastrar_lancamento, name='cadastrar_lancamento'),
    path('listar_lancamentos/', views.listar_lancamentos, name='listar_lancamentos'),
    path('painel_geral/', views.painel_geral, name='painel_geral'),
    path('visualizar_artista/<int:pk>/', views.visualizar_artista, name='visualizar_artista'),
    path('visualizar_lancamento/<int:pk>/', views.visualizar_lancamento, name='visualizar_lancamento'),
    path('manifesto/', views.manifesto, name='manifesto'),

]
