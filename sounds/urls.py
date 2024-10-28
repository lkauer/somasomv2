from django.urls import path
from . import views

app_name = 'sounds'

urlpatterns = [
    path('add_sound/', views.add_sound, name='add_sound'),
    path('edit_sound/<int:pk>/', views.edit_sound, name='edit_sound'),
    path('delete_sound/<int:pk>/', views.delete_sound, name='delete_sound'),
    path('list_sounds/', views.list_sounds, name='list_sounds'),
    path('sound/<int:pk>/', views.sound, name='sound'),
]
