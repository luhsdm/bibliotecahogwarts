from django.contrib import admin
from django.urls import path, include
from adminlte import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('livro/', include('livro.urls')),
    path('ver_livros/', views.ver_livros, name='ver_livros'),


]
