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

    @property
    def status_formatado(self):
        for id, descricao in STATUS:
            if self.status == id:
                return descricao
            return self.status
    
class TipoDespesa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    
    def __str__(self) -> str:
        return self.nome
    
    @property
    def status_formatado(self):
        for id, descricao in STATUS:
            if self.status == id:
                return descricao
            return self.status


class TipoReceita(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    
    def __str__(self) -> str:
        return self.nome
    
    @property
    def status_formatado(self):
        for id, descricao in STATUS:
            if self.status == id:
                return descricao
            return self.status
    