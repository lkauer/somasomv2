from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # outras rotas...
    path('', views.index, name='index'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('topic/<int:pk>/', views.topic, name='topic'),
    path('edit_topic/<int:pk>/', views.edit_topic, name='edit_topic'),
    path('delete_topic/<int:pk>/', views.delete_topic, name='delete_topic'),
    path('topic/<int:pk>/add_post/', views.add_post_topic, name='add_post_topic'),
    path('topic/<int:pk>/delete_post/', views.delete_post_topic, name='delete_post_topic'),
]

    