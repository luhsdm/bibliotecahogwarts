from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'django_adminlte/adminlte/login.html')


def cadastro(request):
    return render(request, 'django_adminlte/adminlte/cadastro.html')


def login(request):
    return render(request, 'django_adminlte/adminlte/login.html')


def ver_livros(request):
    return render(request, 'django_adminlte/adminlte/ver_livros.html')

def ver_emprestimos(request):
    return render(request, 'django_adminlte/adminlte/ver_emprestimos.html')

def ver_devolucao(request):
    return render(request, 'django_adminlte/adminlte/ver_devolucao.html')
