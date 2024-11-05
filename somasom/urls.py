from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views as myapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),  # Rotas gerais e do painel
    path('artists/', include('artists.urls', namespace='artists')),  # Rotas do app de artists
    path('sounds/', include('sounds.urls', namespace='sounds')),  # Rotas do app de sounds
    path('signup/', myapp_views.signup, name='signup'),
    path('', include('myapp.urls'), name='index'),  # Redireciona para o índice principal
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('community/', include('community.urls', namespace='community')),  # Rotas do app de community
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
