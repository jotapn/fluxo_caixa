from django.db import models

class Status(models.TextChoices):
    ATIVO = 'AT', "Ativo"
    INATIVO = 'IN', "Inativo"

class Operacoes(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices, 
                                default=Status.ATIVO)

    def __str__(self) -> str:
        return self.nome

    @property
    def status_formatado(self):
        return dict(Status.choices).get(self.status, self.status)

class TipoPagamento(Operacoes): 
    ...

class TipoDespesa(Operacoes):
    ...

class TipoReceita(Operacoes):
    ...