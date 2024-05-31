from django.shortcuts import render

# Create your views here.
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
