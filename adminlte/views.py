from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

#@login_required
def home(request):
    return render(request, 'home.html' )

#@login_required
def ver_livros(request):
    return render(request, 'ver_livros.html')

#@login_required
def ver_emprestimos(request):
    return render(request, 'ver_emprestimos.html')

#@login_required
def ver_devolucao(request):
    return render(request, 'ver_devolucao.html')
