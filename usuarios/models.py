from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=40)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=True)

    def abreviar_nome(self):
        partes_nome = self.nome.split()
        if len(partes_nome) > 1:
            primeiro_nome = partes_nome[0]
            segundo_nome = partes_nome[1]
            nome_abreviado = f"{primeiro_nome} {segundo_nome[0]}."
            return nome_abreviado
        else:
            return self.nome

    def __str__(self):
        return self.abreviar_nome()
