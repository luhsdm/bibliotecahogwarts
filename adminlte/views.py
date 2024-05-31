from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from livro.models import Livros

def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html' )

def ver_livros(request):
    livros = Livros.objects.all()
    return render(request, 'ver_livros.html', {'livros': livros})

def ver_emprestimos(request):
    return render(request, 'ver_emprestimos.html')

def ver_devolucao(request):
    return render(request, 'ver_devolucao.html')

def buscar_livros(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        livros = Livros.objects.filter(nome__contains=search_query)
        resultado_busca = livros.count()
        return render(request, 'buscar_livros.html', {'livros': livros, 'resultado_busca': resultado_busca})
    else:
        return render(request, 'buscar_livros.html')
