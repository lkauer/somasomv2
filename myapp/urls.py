from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_artist/', views.add_artist, name='add_artist'),
    path('edit_artist/<int:pk>/', views.edit_artist, name='edit_artist'),
    path('edit_sound/<int:pk>/', views.edit_sound, name='edit_sound'),
    path('delete_artist/<int:pk>/', views.delete_artist, name='delete_artist'),
    path('delete_sound/<int:pk>/', views.delete_sound, name='delete_sound'),
    path('list_artists/', views.list_artists, name='list_artists'),
    path('add_sound/', views.add_sound, name='add_sound'),
    path('list_sounds/', views.list_sounds, name='list_sounds'),
    path('general_panel/', views.general_panel, name='general_panel'),
    path('artist/<int:pk>/', views.artist, name='artist'),
    path('sound/<int:pk>/', views.sound, name='sound'),
    path('search_results/', views.search_results, name='search_results'),
    # path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('about/', views.about, name='about'),
]
