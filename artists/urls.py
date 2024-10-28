from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('add_artist/', views.add_artist, name='add_artist'),
    path('edit_artist/<int:pk>/', views.edit_artist, name='edit_artist'),
    path('delete_artist/<int:pk>/', views.delete_artist, name='delete_artist'),
    path('list_artists/', views.list_artists, name='list_artists'),
    path('artist/<int:pk>/', views.artist, name='artist'),
]
