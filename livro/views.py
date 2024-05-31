from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from livro.models import Categoria, Devolucao, Livros, Emprestimos
from .forms import CadastroLivro, EmprestimosLivrosForm
from usuarios.models import Usuario
from django.shortcuts import redirect, render
from django.db.models import Q
from datetime import datetime, timedelta
import holidays
from django.utils.timezone import make_aware
from django.template.loader import render_to_string
from django.core import serializers
from django.contrib.auth.decorators import login_required


def home(request):
    usuario_id = request.session.get('usuario')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livros.objects.filter(usuario=usuario)
        total_livros = Livros.objects.count()
        total_emprestimos = Emprestimos.objects.count()
        form = CadastroLivro()
        form.fields['categoria'].queryset = Categoria.objects.filter(
            usuario=usuario)
        form_categoria = Categoria()
        usuarios = Usuario.objects.all()
        categorias = Categoria.objects.all()
        total_devolucao = Devolucao.objects.count()

        # Modificação aqui: incluir livros com quantidade disponível maior que zero
        livros_emprestar = Livros.objects.filter(
            usuario=usuario, quantidade__gt=0)

        livros_emprestados = Livros.objects.filter(
            usuario=usuario, emprestado=True)

        return render(request, 'home.html', {'livros': livros,
                                                      'usuario_logado': usuario_id,
                                                      'form': form,
                                                      'status_categoria': status_categoria,
                                                      'form_categoria': form_categoria,
                                                      'usuarios': usuarios,
                                                      'categorias': categorias,
                                                      'livros_emprestar': livros_emprestar,
                                                      'total_livros': total_livros,
                                                      'total_usuarios': usuarios.count(),
                                                      'total_emprestimos': total_emprestimos,
                                                      'livros_emprestados': livros_emprestados,
                                                      'total_devolucao': total_devolucao})
    else:
        return redirect('/usuarios/login/?status=2')


# == ÁREA CATEGORIA ==#


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
        return HttpResponse('Erro.')


# == FIM ÁREA CATEGORIA ==#


# == ÁREA LIVROS ==#
@login_required
def ver_livros(request):
    return render(request, 'ver_livros')

@login_required
def buscar_livros(request):
    search_query = request.POST.get('search_query', '')
    livros = Livros.objects.filter(nome__contains=search_query)

    return render(request, 'buscar_livros.html', {'livros': livros, 'resultado_busca': livros.count()})


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST, request.FILES)

        if form.is_valid():
            novo_livro = form.save(commit=False)
            novo_livro.usuario = Usuario.objects.get(
                id=request.session['usuario'])
            novo_livro.save()
            return redirect('home')
        else:
            return render(request, 'templates/home.html', {'form': form})
    else:
        form = CadastroLivro()
        categorias = Categoria.objects.all()
        return render(request, 'templates/home.html', {'form': form, 'categorias': categorias})


def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    categoria_id = request.POST.get('categoria_id')

    categoria = Categoria.objects.get(id=categoria_id)
    livro = Livros.objects.get(id=livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.categoria = categoria
        livro.save()
        return redirect('ver_livros')
    else:
        return redirect('/usuarios/sair')


def excluir_livro(request, id):
    livro = Livros.objects.get(id=id).delete()
    return redirect('home')


# == FIM ÁREA LIVROS ==#


# == ÁREA DEVOLUÇÃO ==#


def devolver_livro(request):
    if request.method == 'POST':
        id_livro_devolver = request.POST.get('livro_devolvido')
        livro_devolver = Livros.objects.get(id=id_livro_devolver)

        if livro_devolver.emprestado:
            # Filtrando empréstimos pelo livro e pelo status 'E' (emprestado)
            emprestimos = Emprestimos.objects.filter(
                livro=livro_devolver, status='E')

            if emprestimos.exists():
                # Iterando sobre cada empréstimo encontrado
                for emprestimo in emprestimos:
                    devolucao = Devolucao(emprestimo=emprestimo)
                    devolucao.save()

                    emprestimo.status = 'D'  # Definindo o status como 'Devolvido'
                    emprestimo.save()

                livro_devolver.emprestado = False
                livro_devolver.save()

                # Atualiza o saldo do livro
                livro_devolver.quantidade += emprestimos.count()
                livro_devolver.save()

                return redirect('home')
            else:
                return HttpResponse("Não foram encontrados empréstimos para este livro.")
        else:
            return HttpResponse("Este livro não está atualmente emprestado.")
    else:
        return HttpResponse("Método de solicitação não permitido para esta URL.")


def listar_usuario_por_livro_para_devolucao(request):
    if request.method == 'GET' and 'livro_devolvido' in request.GET:
        livro_id = request.GET.get('livro_devolvido', None)
        if livro_id:
            try:
                livro = Livros.objects.get(id=livro_id)
                # Filtrando empréstimos apenas pelo status de empréstimo 'E' (emprestado)
                emprestimos = Emprestimos.objects.filter(livro=livro, status='E')
                if emprestimos.exists():
                    # Construindo a lista de usuários associados apenas aos empréstimos em andamento
                    usuarios_com_o_livro = [{'pk': emprestimo.nome_emprestado.pk, 'fields': {
                        'nome': emprestimo.nome_emprestado.nome}} for emprestimo in emprestimos if emprestimo.nome_emprestado]
                    return JsonResponse({'usuarios_com_o_livro': usuarios_com_o_livro})
                else:
                    return JsonResponse({'usuarios_com_o_livro': []})
            except Livros.DoesNotExist:
                pass
        else:
            return JsonResponse({'error': 'O parâmetro livro_devolvido está ausente ou vazio.'})
    return JsonResponse({'usuarios_com_o_livro': []})


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


# == FIM ÁREA DEVOLUÇÃO ==#


# == ÁREA EMPRESTIMOS ==#


def cadastrar_emprestimo(request):
    if request.method == 'POST':
        livro_emprestado_id = request.POST.get('livro_emprestado')
        data_emprestimo = request.POST.get('data_emprestimo')
        usuario_formulario = request.POST.get('usuario_emprestado')

        if not data_emprestimo:
            return HttpResponse("A data de empréstimo é obrigatória.")

        if not livro_emprestado_id:
            return HttpResponse("O livro emprestado é obrigatório.")

        if not usuario_formulario:
            return HttpResponse("O usuário é obrigatório.")

        livro = Livros.objects.get(id=livro_emprestado_id)
        if livro.quantidade <= 0:
            return HttpResponse("Este livro não está disponível para empréstimo no momento.")

        data_devolucao = calcular_data_devolucao(data_emprestimo)
        data_emprestimo_obj = datetime.strptime(data_emprestimo, '%Y-%m-%d')
        data_devolucao_obj = datetime.strptime(data_devolucao, '%Y-%m-%d')

        data_emprestimo_consciente = make_aware(data_emprestimo_obj)
        data_devolucao_consciente = make_aware(data_devolucao_obj)

        usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        usuario_emprestimo = Usuario.objects.get(id=usuario_formulario)

        emprestimo = Emprestimos(nome_emprestado=usuario_emprestimo,
                                 usuario=usuario_logado,
                                 livro_id=livro_emprestado_id,
                                 data_emprestimo=data_emprestimo_consciente,
                                 data_devolucao=data_devolucao_consciente,
                                 status='E')  # Definindo o status como "Emprestado"
        emprestimo.save()

        livro.emprestado = True
        livro.quantidade -= 1
        livro.save()

        return redirect('home')
    else:
        return HttpResponseBadRequest("Método não permitido para esta rota.")
    
@login_required
def ver_emprestimos(request):
    if request.method == 'GET':
        emprestimos = Emprestimos.objects.all()
        for emprestimo in emprestimos:
            if emprestimo.nome_emprestado:
                emprestimo.nome_emprestado.nome = emprestimo.nome_emprestado.abreviar_nome()

        print("Quantidade de empréstimos:", len(emprestimos))
        return render(request, 'templates/ver_emprestimos.html', {'emprestimos': emprestimos})
    else:
        form = EmprestimosLivrosForm(request.GET)
        if form.is_valid():
            livro_id = form.cleaned_data['livro']
            livro = Livros.objects.get(id=livro_id)
            emprestimos = Emprestimos.objects.filter(livro=livro)
            return render(request, 'templates/ver_emprestimos.html', {'emprestimos': emprestimos})
        else:
            emprestimos = Emprestimos.objects.all()
            print("Quantidade de empréstimos:", len(emprestimos))
            return render(request, 'templates/ver_emprestimos.html', {'emprestimos': emprestimos})


def buscar_emprestimo(request):
    emprestimos = Emprestimos.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('buscar_emprestimo.html', {
                                'emprestimos': emprestimos})
        return JsonResponse({'html': html})

    return render(request, 'templates/buscar_emprestimo.html', {'emprestimos': emprestimos, 'resultado_busca': emprestimos.count()})


# == FIM ÁREA EMPRESTIMOS ==#
