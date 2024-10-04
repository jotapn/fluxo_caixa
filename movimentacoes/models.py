from django.db import models
from clientes.models import Cliente


STATUS = (
    ("AT", "Ativo"),
    ("IN", "Inativo")
)

SITUACAO = (
    ("PG", "Pago"),
    ("AP", "A pagar")
)


class Banco(models.Model):
    nome = models.CharField(max_length=50)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")
    saldo_atual = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True,auto_created=True, default=0)

    def __str__(self):
        return self.nome


class Tipo(models.Model):
    NOME_TIPO = (
        ("pagamento", "Tipo de Pagamento"),
        ("despesa", "Tipo de Despesa"),
        ("entrada", "Tipo de Entrada"),
    )
    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=10, choices=NOME_TIPO)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")

    def __str__(self):
        return self.nome


class Entrada(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    tipo_pagamento = models.ForeignKey(Tipo, limit_choices_to={'tipo': 'pagamento'}, on_delete=models.PROTECT,related_name='pagamentos')
    tipo_entrada = models.ForeignKey(Tipo, limit_choices_to={'tipo': 'entrada'}, on_delete=models.PROTECT, related_name='entradas')
    situacao = models.CharField(max_length=2, choices=SITUACAO)

    def __str__(self):
        return f'Entrada: {self.valor} - {self.descricao}'


class Saida(models.Model):
    tipo_despesa = models.ForeignKey(Tipo, limit_choices_to={'tipo': 'despesa'}, on_delete=models.PROTECT,related_name='despesas_saida')
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    tipo_pagamento = models.ForeignKey(Tipo, limit_choices_to={'tipo': 'pagamento'}, on_delete=models.PROTECT, related_name='saidas')
    situacao = models.CharField(max_length=2, choices=SITUACAO)

    def __str__(self):
        return f'Saída: {self.valor} - {self.descricao}'
