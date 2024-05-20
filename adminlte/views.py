from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'adminlte/base.html')


def cadastro(request):
    return render(request, 'adminlte/cadastro.html')


def login(request):
    return render(request, 'adminlte/login.html')


def ver_livros(request):
    return render(request, 'adminlte/ver_livros.html')

def ver_emprestimos(request):
    return render(request, 'adminlte/ver_emprestimos.html')
