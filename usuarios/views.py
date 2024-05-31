from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256


def abreviar_nome(nome):
    partes_nome = nome.split()
    if len(partes_nome) > 1:
        primeiro_nome = partes_nome[0]
        sobrenome = partes_nome[-1]
        nome_abreviado = f"{primeiro_nome} {sobrenome[0]}."
        return nome_abreviado
    else:
        return nome


def home(request):
    if 'usuario' not in request.session:
        return redirect('login.html')

    usuario_logado_id = request.session.get('usuario')
    if usuario_logado_id:
        usuario = Usuario.objects.get(pk=usuario_logado_id)
        nome_usuario = abreviar_nome(usuario.nome)
        return render(request, 'templates/home.html', {'nome_usuario': nome_usuario})
    else:
        return redirect('login.html')


def login(request):
    if 'usuario' in request.session:
        return redirect('home.html')
    status = request.GET.get('status')
    nome_usuario = None
    usuario_logado_id = request.session.get('usuario')
    if usuario_logado_id:
        usuario = Usuario.objects.get(pk=usuario_logado_id)
        nome_usuario = abreviar_nome(usuario.nome)
        return redirect('home.html')
    return render(request, 'login.html', {'status': status, 'nome_usuario': nome_usuario})


def cadastro(request):
    if 'usuario' in request.session:
        return redirect('home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        if nome and email and senha:
            if len(senha) < 8:
                return redirect('/usuarios/cadastro/?status=2')

            if Usuario.objects.filter(email=email).exists():
                return redirect('/usuarios/cadastro/?status=3')

            try:
                senha_hash = sha256(senha.encode()).hexdigest()
                novo_usuario = Usuario(
                    nome=nome, cpf=cpf, email=email, senha=senha_hash)
                novo_usuario.save()
                return redirect('/usuarios/cadastro/?status=0')
            except Exception as e:
                print(f"Erro ao salvar novo usuário: {e}")
                return redirect('/usuarios/cadastro/?status=4')
        else:
            return redirect('/usuarios/cadastro/?status=1')
    else:
        return redirect('/usuarios/cadastro/?status=1')


def valida_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        if email and senha:
            senha_hash = sha256(senha.encode()).hexdigest()
            usuario = Usuario.objects.filter(email=email, senha=senha_hash).first()

            if usuario:
                request.session['usuario'] = usuario.id
                return redirect('home')  
            else:
                return redirect('login', status=1)  
        else:
            return HttpResponse("Campos de email e senha não foram fornecidos.")
    else:
        return HttpResponse("Método de requisição inválido.")

def sair(request):
    request.session.flush()
    return redirect('login')
