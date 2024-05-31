from django.contrib import admin
from django.urls import path, include
from adminlte import views
from django.conf.urls.static import static
from django.conf import settings
from livro.views import ver_emprestimos, ver_livros
from usuarios import views as usuarios_views
from adminlte import views as adminlte_views
from usuarios import views as usuarios_views 
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', adminlte_views.login, name='login'),
    path('home/', adminlte_views.home, name='home'),
    path('usuarios/', include('usuarios.urls')),
    path('livro/', include('livro.urls')),
    path('ver_emprestimos/', login_required(ver_emprestimos), name='ver_emprestimos'),
    path('ver_livros/', login_required(ver_livros), name='ver_livros'),
    path('valida_login/', usuarios_views.valida_login, name='valida_login'), 
    # Use o prefixo usuarios_ aqui
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
