from django.http import HttpResponse
from django.shortcuts import redirect, render
from usuarios.models import Usuario
from django import forms
from django.db.models import fields
from .models import Livros, Categoria
from django.db import models
from django import forms
from .models import Livros
from django import forms


class CadastroLivro(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    class Meta:
        model = Livros
        fields = ['nome', 'autor', 'ano_publicacao',
                  'editora', 'quantidade', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'usuario' in self.fields:
            self.fields['usuario'].widget = forms.HiddenInput()


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            return redirect('home')
        else:
            return HttpResponse('Dados inválidos')
    else:
        form = CadastroLivro()
        return render(request, 'home.html', {'form': form})
