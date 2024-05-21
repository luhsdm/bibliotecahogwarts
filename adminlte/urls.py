from django.contrib import admin
from django.urls import path, include
from adminlte import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('livro/', include('livro.urls')),
    path('ver_livros/', views.ver_livros, name='ver_livros'),
    path('ver_emprestimos/', views.ver_emprestimos, name='ver_emprestimos'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
