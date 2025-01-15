from datetime import timedelta
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from operacoes.models import NaturezaFinanceira, CentroDeCusto
from cadastro.models import Cadastro
from bancos.models import ContaBancaria

imposto_cadastrado = 0.06

class TipoMovimentacao(models.TextChoices):
    RECEBER = "RE", "Receita"
    PAGAR = "PA", "Pagar"
    
class FormaRecebimento(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome



class Movimentacao(models.Model):
    tipo_movimentacao = models.CharField(
        max_length=2,
        choices=TipoMovimentacao.choices,
        verbose_name="Tipo de Movimentação"
    )
    natureza_financeira = models.ForeignKey(NaturezaFinanceira, verbose_name=("Natureza Financeira"), on_delete=models.PROTECT)
    centro_de_custo = models.ForeignKey(CentroDeCusto, verbose_name=("Centro de Custo"), on_delete=models.PROTECT)
    # rateio_cc = 
    data_movimentacao = models.DateField(verbose_name="Data Movimentação", default=timezone.now)
    descricao = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    parcelado = models.BooleanField(
        default=False,
        verbose_name="Parcelado"
    )
    # imposto = valor*imposto_cadastrado
    forma_recebimento = models.ForeignKey(FormaRecebimento, on_delete=models.PROTECT)
    data_vencimento = models.DateField()
    cadastro = models.ForeignKey(Cadastro, verbose_name=("Cliente/Fornecedor"), on_delete=models.PROTECT)
    conta_bancaria = models.ForeignKey(ContaBancaria, verbose_name=("Conta Bancária"), on_delete=models.PROTECT)

    @property
    def tipo_movimentacao(self):
        return self.natureza_financeira.tipo

    @property
    def valor_liquido(self):
        return self.valor  # Por enquanto, igual ao valor bruto. Esperando definiçao do calculo do imposto
    
    def gerar_parcela(self, total_parcela, data_inicial):
        if not self.parcelado:
            return  # Não gera parcelas se não for parcelado
        
        valor_parcela = self.valor / total_parcela
        for i in range(1, total_parcela +1):
            Parcela.objects.create(
                movimentacao = self,
                numero = i,
                valor = valor_parcela,
                data_vencimento = data_inicial + timedelta(days=(30 * i))
            )

    def clean(self):
        super().clean()

        # Validar rateio
        if self.rateios.exists():
            total_valor = sum(rateio.valor or 0 for rateio in self.rateios.all() if rateio.tipo_rateio == TipoRateio.VALOR)
            total_percentual = sum(rateio.percentual or 0 for rateio in self.rateios.all() if rateio.tipo_rateio == TipoRateio.PORCENTAGEM)

            if any(rateio.tipo_rateio == TipoRateio.VALOR for rateio in self.rateios.all()):
                if total_valor != self.valor:
                    raise ValidationError("A soma dos valores do rateio deve ser igual ao valor total da movimentação.")

            if any(rateio.tipo_rateio == TipoRateio.PORCENTAGEM for rateio in self.rateios.all()):
                if total_percentual != 100:
                    raise ValidationError("A soma dos percentuais do rateio deve ser igual a 100%.")



class TipoRateio(models.TextChoices):
    VALOR = "VA", "Valor"
    PORCENTAGEM = "PO", "Porcentagem"

class RateioCentroDeCusto(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, related_name="rateios", on_delete=models.CASCADE)
    centro_de_custo = models.ForeignKey(CentroDeCusto, verbose_name=("Centro de Custo"), on_delete=models.PROTECT)
    tipo_rateio = models.CharField(
        max_length=2,
        choices=TipoRateio.choices,
        default=TipoRateio.VALOR,  # Valor como padrão
        verbose_name="Tipo de Rateio"
    )
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Valor do Rateio"
    )
    percentual = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Percentual de Rateio"  # Exemplo: 50.00 para 50%
    )

    def __str__(self):
        return f"{self.centro_de_custo} - {self.tipo_rateio}: {self.valor or self.percentual}%"
    
    def clean(self):
        super().clean()

        if self.tipo_rateio == TipoRateio.VALOR and self.valor is None:
            raise ValidationError("Para o tipo de rateio por valor, o campo 'valor' deve ser preenchido.")
        elif self.tipo_rateio == TipoRateio.PORCENTAGEM and self.porcentagem is None:
            raise ValidationError("Para o tipo de rateio por porcentagem, o campo 'percentual' deve ser preenchido.")
    
    
class Parcela(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, related_name="parcelas", on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(verbose_name="Número de Parcelas")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return f"Parcela {self.numero} - {self.valor}"