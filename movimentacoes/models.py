from django.db import models, transaction
from bancos.models import ContaBancaria
from clientes.models import Cliente
from operacoes.models import TipoReceita, TipoDespesa, TipoPagamento


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

    def ajustar_saldo_conta(self, sinal):
        """Ajusta o saldo da conta de acordo com o valor e o sinal"""
        if sinal == "-":
            self.conta.saldo_atual -= self.valor
        elif sinal == "+":
            self.conta.saldo_atual += self.valor
        self.conta.save()

    @transaction.atomic
    def save(self, *args, **kwargs):
        ''' Verifica se é uma nova movimentação ou se a situação foi alterada para "Pago" '''
        if self.pk is None or self.__class__.objects.get(pk=self.pk).situacao != Situacao.PAGO:
            # Ajusta o saldo da conta apenas se a situação for 'Pago'
            if self.situacao == Situacao.PAGO:
                sinal = "+" if isinstance(self, Entrada) else "-"
                self.ajustar_saldo_conta(sinal)
        
        elif self.situacao == Situacao.A_PAGAR:
            sinal = "-" if isinstance(self, Entrada) else "+"
            self.ajustar_saldo_conta(sinal)


        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.situacao == Situacao.PAGO:
            '''Atualizar o saldo da conta bancária associada caso seja uma movimentação paga'''
            sinal = "-" if isinstance(self, Entrada) else "+"
            self.ajustar_saldo_conta(sinal)
        super().delete(*args, **kwargs)  # Excluir a Movimentaçao

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
    