from .models import Emprestimos
from usuarios.models import Usuario
from django import forms
from .models import Livros, Categoria
from django import forms
from .models import Livros
from django import forms


class CadastroLivro(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'usuario' in self.fields:
            self.fields['usuario'].widget = forms.HiddenInput()

    class Meta:
        model = Livros
        fields = ['nome', 'imagem', 'autor', 'ano_publicacao', 'categoria', 'editora', 'quantidade']
        widgets = {'categoria': forms.Select(attrs={'class': 'form-control'})}  # Adicionando classe CSS para o campo de categoria

        # Limitando a consulta ao banco de dados para as categorias
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['categoria'].queryset = Categoria.objects.all()


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'telefone', 'email', 'senha']


class EmprestimosLivrosForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        emprestimos = Emprestimos.objects.all().distinct('livro')
        
        choices = [(emprestimo.livro.id, emprestimo.livro.nome) for emprestimo in emprestimos]
        
        self.fields['livro'] = forms.ChoiceField(choices=choices)
        
        for emprestimo in emprestimos:
         
            label = f"{emprestimo.livro.nome} - Empréstimo: {emprestimo.data_emprestimo} - Devolução: {emprestimo.data_devolucao} - Usuário: {emprestimo.usuario.nome}"
         
            self.fields['livro'].choices.append((emprestimo.livro.id, label))