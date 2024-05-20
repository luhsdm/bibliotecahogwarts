from django.http import JsonResponse
from livro.models import Categoria
from .models import Emprestimos, Livros
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from livro.models import Emprestimos, Livros, Categoria
from .forms import CadastroLivro
from django.db.models import Q
from usuarios.models import Usuario
import holidays

def home(request):
    usuario_id = request.session.get('usuario')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livros.objects.filter(usuario=usuario)
        total_livros = Livros.objects.count()
        total_usuarios = Usuario.objects.count()
        total_emprestimos = Emprestimos.objects.count()
        form = CadastroLivro()
        form.fields['categoria'].queryset = Categoria.objects.filter(
            usuario=usuario)
        form_categoria = Categoria()
        usuarios = Usuario.objects.all()
        categorias = Categoria.objects.all()

        livros_emprestar = Livros.objects.filter(
            usuario=usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(
            usuario=usuario).filter(emprestado=True)

        return render(request, 'adminlte/home.html', {'livros': livros,
                                                      'usuario_logado': usuario_id,
                                                      'form': form,
                                                      'status_categoria': status_categoria,
                                                      'form_categoria': form_categoria,
                                                      'usuarios': usuarios,
                                                      'categorias': categorias,
                                                      'livros_emprestar': livros_emprestar,
                                                      'total_livros': total_livros,
                                                      'total_usuarios': total_usuarios,
                                                      'total_emprestimos': total_emprestimos,
                                                      'livros_emprestados': livros_emprestados})
    else:
        return redirect('/usuarios/login/?status=2')

def ver_livros(request):
    return render(request, 'ver_livros')

def buscar_livro(request):
    search_query = request.POST.get('search_query', '')
    livros = Livros.objects.filter(nome__contains=search_query) 

    return render(request,'adminlte/buscar_livro.html', {'livros': livros, 'resultado_busca': livros.count()})

def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)

        if form.is_valid():
            novo_livro = form.save(commit=False)
            novo_livro.usuario = Usuario.objects.get(
                id=request.session['usuario'])
            novo_livro.save()
            return redirect('home')
        else:
            print(form.errors)
            form = CadastroLivro()
            return render(request, 'adminlte/home.html', {'form': form})
    else:
        form = CadastroLivro()
        categorias = Categoria.objects.all()
        return render(request, 'adminlte/home.html', {'form': form, 'categorias': categorias})


def excluir_livro(request, id):
    livro = Livros.objects.get(id=id).delete()
    return redirect('home')


def cadastrar_categoria(request):
    form = Categoria(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('home?cadastro_categoria=1')
    else:
        return HttpResponse('Pare de ser um usuário malandrinho. Não foi desta vez.')


def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado_id = request.POST.get('livro_emprestado')
        data_emprestimo = request.POST.get('data_emprestimo')

        if not data_emprestimo:
            return HttpResponse("A data de empréstimo é obrigatória.")

        if not livro_emprestado_id:
            return HttpResponse("O livro emprestado é obrigatório.")

        livro = Livros.objects.get(id=livro_emprestado_id)
        if livro.quantidade <= 0:
            return HttpResponse("Este livro não está disponível para empréstimo no momento.")

        def calcular_data_devolucao(data_emprestimo):
            def is_business_day(date):
                br_holidays = holidays.Brazil()
                return date.weekday() < 5 and date not in br_holidays

            data_emprestimo_obj = datetime.strptime(
                data_emprestimo, '%Y-%m-%d')
            dias_adicionais = 0
            while dias_adicionais < 4:
                data_emprestimo_obj += timedelta(days=1)
                if is_business_day(data_emprestimo_obj):
                    dias_adicionais += 1
            return data_emprestimo_obj.strftime('%Y-%m-%d')

        data_devolucao = calcular_data_devolucao(data_emprestimo)

        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo=nome_emprestado_anonimo,
                                     livro_id=livro_emprestado_id,
                                     data_emprestimo=data_emprestimo,
                                     data_devolucao=data_devolucao)
        else:
            emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado,
                                     livro_id=livro_emprestado_id,
                                     data_emprestimo=data_emprestimo,
                                     data_devolucao=data_devolucao)
        emprestimo.save()

        livro.quantidade -= 1
        livro.save()

        return redirect('home')


def devolver_livro(request):
    if request.method == 'POST':
        id_livro_devolver = request.POST.get('id_livro_devolver')
        livro_devolver = Livros.objects.get(id=id_livro_devolver)
        livro_devolver.emprestado = False
        livro_devolver.save()

        emprestimo_devolver = Emprestimos.objects.get(
            Q(livro=livro_devolver) & Q(data_devolucao=None))
        emprestimo_devolver.data_devolucao = datetime.now()
        emprestimo_devolver.save()

        return redirect('home')
    else:
        return HttpResponse("Método de solicitação não permitido para esta URL.")


def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')

    categoria = Categoria.objects.get(id=categoria_id)
    livro = Livros.objects.get(id=livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()
        return redirect('ver_livros')
    else:
        return redirect('/usuarios/sair')


def seus_emprestimos(request):
    usuario = Usuario.objects.get(id=request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado=usuario)

    return render(request, 'adminlte/ver_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                             'emprestimos': emprestimos})


def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')

    emprestimo = Emprestimos.objects.get(id=id_emprestimo)
    emprestimo.avaliacao = opcoes
    emprestimo.save()
    return redirect(f'/adminlte/templates/adminlte/ver_livros.html{id_livro}')


def buscar_livros(request):
    try:

        query = request.GET.get('q', '')
        livros = Livros.objects.filter(nome__icontains=query)

        data = [{'id': livro.id, 'nome': livro.nome} for livro in livros]

        return JsonResponse(data, safe=False)

    except Exception as e:

        print(f"Erro ao buscar livros: {str(e)}")
        return JsonResponse({'error': 'Ocorreu um erro ao buscar os livros.'}, status=500)
