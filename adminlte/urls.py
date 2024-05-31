from django.contrib import admin
from django.urls import path, include
from adminlte import views
from django.conf.urls.static import static
from django.conf import settings
from usuarios import views as usuarios_views
from adminlte import views as adminlte_views
from usuarios import views as usuarios_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', adminlte_views.login, name='login'),
    path('home/', adminlte_views.home, name='home'),
    path('usuarios/', include('usuarios.urls')),
    path('livro/', include('livro.urls')),
    path('ver_livros', views.ver_livros, name='ver_livros'),
    path('ver_emprestimos', views.ver_emprestimos, name="ver_emprestimos"),
    path('valida_login/', usuarios_views.valida_login, name='valida_login'), 
    path('buscar_emprestimo/', views.buscar_emprestimo, name='buscar_emprestimo'),# Use o prefixo usuarios_ aqui
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
