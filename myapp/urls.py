from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar_artista/', views.cadastrar_artista, name='cadastrar_artista'),
    path('editar_artista/<int:pk>/', views.editar_artista, name='editar_artista'),
    path('editar_som/<int:pk>/', views.editar_som, name='editar_som'),
    path('excluir_artista/<int:pk>/', views.excluir_artista, name='excluir_artista'),
    path('excluir_som/<int:pk>/', views.excluir_som, name='excluir_som'),
    path('listar_artistas/', views.listar_artistas, name='listar_artistas'),
    path('cadastrar_som/', views.cadastrar_som, name='cadastrar_som'),
    path('listar_sons/', views.listar_sons, name='listar_sons'),
    path('painel_geral/', views.painel_geral, name='painel_geral'),
    path('visualizar_artista/<int:pk>/', views.visualizar_artista, name='visualizar_artista'),
    path('visualizar_som/<int:pk>/', views.visualizar_som, name='visualizar_som'),
]
