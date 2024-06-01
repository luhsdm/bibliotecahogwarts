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
    return render(request, 'ver_livros.html')

def ver_emprestimos(request):
    return render(request, 'ver_emprestimos.html')

def ver_devolucao(request):
    return render(request, 'ver_devolucao.html')

def buscar_livros(request):
    livros = []
    resultado_busca = 0

    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            # Usando __icontains para pesquisa case-insensitive
            livros = Livros.objects.filter(nome__icontains=search_query)
            resultado_busca = livros.count()
    return render(request, 'buscar_livros.html', {'livros': livros, 'resultado_busca': resultado_busca})
