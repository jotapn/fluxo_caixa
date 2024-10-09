from django.db import models

STATUS = (
    ("AT", "Ativo"),
    ("IN", "Inativo")
)

class TipoPagamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    
    def __str__(self) -> str:
        return self.nome
    
class TipoDespesa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    
    def __str__(self) -> str:
        return self.nome


class TipoReceita(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    
    def __str__(self) -> str:
        return self.nome
    