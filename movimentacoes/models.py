from django.db import models, transaction
from bancos.models import ContaBancaria
from clientes.models import Cliente
from operacoes.models import TipoReceita, TipoDespesa, TipoPagamento
from movimentacoes.services import deletar_movimentacao, salvar_movimentacao


class Situacao(models.TextChoices):
    PAGO = 'PG', "Pago"
    A_PAGAR = 'AP', "A pagar"

class Movimentacoes(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    conta = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    tipo_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.PROTECT, related_name='pagamentos')
    situacao = models.CharField(max_length=2, choices=Situacao.choices, default=Situacao.A_PAGAR)

    class Meta:
        ordering = ['-data']

    @transaction.atomic
    def save(self, *args, **kwargs):
        tipo_operacao = True if isinstance(self, Entrada) else False
        salvar_movimentacao(self, Situacao, tipo_operacao)
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        tipo_operacao = True if isinstance(self, Entrada) else False
        deletar_movimentacao(self, Situacao, tipo_operacao)
        super().delete(*args, **kwargs)

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def situacao_formatado(self):
        return dict(Situacao.choices).get(self.situacao, self.situacao)

class Entrada(Movimentacoes):
    tipo_receita = models.ForeignKey(TipoReceita, on_delete=models.PROTECT, related_name='receitas', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return f'Entrada: {self.valor} - {self.descricao}'


class Saida(Movimentacoes):
    tipo_despesa = models.ForeignKey(TipoDespesa, on_delete=models.PROTECT,related_name='despesas')

    def __str__(self):
        return f'Saída: {self.valor} - {self.descricao}'
    