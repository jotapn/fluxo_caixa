from django.db import models
from django.utils import timezone
from operacoes.models import NaturezaFinanceira, CentroDeCusto
from cadastro.models import Cadastro
from bancos.models import ContaBancaria

imposto_cadastrado = 0.06

class TipoMovimentacao(models.TextChoices):
    RECEBER = "RE", "Receita"
    PAGAR = "PA", "Pagar"

class Movimentacao(models.Model):
    natureza_financeira = models.ForeignKey(NaturezaFinanceira, verbose_name=("Natureza Financeira"), on_delete=models.PROTECT)
    # tipo_movimentacao = natureza_financeira.tipo
    centro_de_custo = models.ForeignKey(CentroDeCusto, verbose_name=("Centro de Custo"), on_delete=models.PROTECT)
    # rateio_cc = 
    data_movimentacao = models.DateField(verbose_name="Data Movimentação", default=timezone.now)
    descricao = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    # parcelas = 
    # imposto = valor*imposto_cadastrado
    # valor_liquido = valor-imposto
    # forma_recebimento = 
    data_vencimento = models.DateField()
    cadastro = models.ForeignKey(Cadastro, verbose_name=("Cliente/Fornecedor"), on_delete=models.PROTECT)
    conta_bancaria = models.ForeignKey(ContaBancaria, verbose_name=("Conta Bancária"), on_delete=models.PROTECT)
