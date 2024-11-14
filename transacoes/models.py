from django.db import models, transaction
from django.utils.timezone import datetime
from bancos.models import ContaBancaria
from clientes.models import Cliente
from operacoes.models import TipoReceita, TipoDespesa, TipoPagamento
from transacoes.services import deletar_movimentacao, salvar_movimentacao


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
    


#--------------------------------------------------------------------------------------
class Status(models.TextChoices):
    ATIVO = 'AT', "Ativo"
    INATIVO = 'IN', "Inativo"


class TipoTransacao(models.TextChoices):
    RECEITA = 'RE', "Receita"
    DESPESA = 'DE', "Despesa"
    INVESTIMENTO = "IV", "Investimento"
    TRANSFERENCIA_ENTRE_CONTA = "TC", "Transferência entre contas"


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    tipo_transacao = models.CharField(max_length=2, choices=TipoTransacao.choices, verbose_name="Tipo Transação")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.nome}"


class Transacao(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    titulo = models.CharField(max_length=100, verbose_name="Título")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor")
    tipo_transacao = models.CharField(max_length=2, choices=TipoTransacao.choices, verbose_name="Tipo Transação")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='transacao_categoria', verbose_name="Categoria")
    classificacao = models.CharField(max_length=2, choices=(("VA", "Variável"), ("FX", "Fixa")), null=True, blank=True, verbose_name="Classificação")
    metodo_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.PROTECT, related_name='transacao_metodo', verbose_name="Método Pagamento")
    data = models.DateField(default=datetime.now, verbose_name="Data")
    situacao = models.CharField(max_length=2, choices=Situacao.choices, default=Situacao.A_PAGAR, verbose_name="Situação")

    class Meta:
        ordering = ['-data']
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def situacao_formatado(self):
        return dict(Situacao.choices).get(self.situacao, self.situacao)
    

    def __str__(self):
        tipo = dict(TipoTransacao.choices).get(self.tipo_transacao, self.tipo_transacao)
        return f'{tipo}: {self.titulo} - {self.valor_formatado}'