from django.db import models
from django.db.models.base import Model
from usuarios.models import Usuario


class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    ano_publicacao = models.DateField()
    editora = models.CharField(max_length=30)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    quantidade = models.IntegerField(default=0)
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    imagem = models.ImageField(upload_to='capa_livro/', null=True, blank=True)
    data_emprestimo = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.nome


class Emprestimos(models.Model):

    nome_emprestado = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_emprestimo = models.DateTimeField()
    data_devolucao = models.DateTimeField(blank=True, null=True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='emprestimos_usuario')
    STATUS_CHOICES = (
        ('E', 'Emprestado'),
        ('D', 'Devolvido'),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='E')

    class Meta:
        verbose_name = 'Emprestimo'

    def __str__(self) -> str:
        return f"{self.nome_emprestado} | {self.livro}"


class Devolucao(models.Model):
    emprestimo = models.ForeignKey(Emprestimos, on_delete=models.CASCADE)
    data_devolucao = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Devolução'

    def __str__(self) -> str:
        return f"{self.emprestimo.livro} | {self.data_devolucao}"
