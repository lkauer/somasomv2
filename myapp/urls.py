from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('general_panel/', views.general_panel, name='general_panel'),
    path('search_results/', views.search_results, name='search_results'),
    path('about/', views.about, name='about'),
]

