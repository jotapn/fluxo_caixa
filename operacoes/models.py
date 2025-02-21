from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from mptt.models import MPTTModel, TreeForeignKey
from cadastro.models import Pessoa, Atributos

class CentroDeCusto(MPTTModel):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=50)
    responsavel = models.ForeignKey(
        Pessoa,
        null=True, blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={"atributos__tipo": Atributos.COLABORADOR},
        related_name="centros_responsaveis"
        )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="subcentros"
    )
    status = models.BooleanField(default=True)


    def clean(self):
        super().clean()
        if self.responsavel and not self.responsavel.atributos.filter(tipo=Atributos.COLABORADOR).exists():
            raise ValidationError("O responsável deve ser um cadastro com o atributo de Colaborador.")
        
    def __str__(self):
        return self.titulo
        
class TipoNatureza(models.TextChoices):
    SINTETICA = "ST", _("Sintética")
    ANALITICA = "AN", _("Analítica")

class SinalNatureza(models.TextChoices):
    CREDITO = "CR", _('Crédito')            #ENTRADA DE CAPITAL
    DEBITO = "DB", _("Débito")              #SAIDA DE CAPITAL
    TRANSITORIA = "TR", _("Transitória")    #TRANSFERENCIAS DE CAPITAL ENTRE CONTAS


class NaturezaFinanceira(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TipoNatureza.choices)
    sinal = models.CharField(max_length=2, choices=SinalNatureza.choices)
    grupo = TreeForeignKey(
        "self", 
        on_delete=models.PROTECT,
        null=True, blank=True,
        )
    
    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if self.tipo == TipoNatureza.ANALITICA and not self.grupo:
            raise ValidationError(_("Naturezas do tipo Analítica devem estar vinculadas a um grupo do tipo Sintética."))
        
        if self.grupo and self.grupo.tipo != TipoNatureza.SINTETICA:
            raise ValidationError(_("O grupo deve ser uma Natureza do tipo Sintética."))
        
    class Meta:
        verbose_name = "Natureza Financeira"
        verbose_name_plural = "Naturezas Financeiras"

    def __str__(self):
        return self.titulo
    

class TipoRateio(models.TextChoices):
    VALOR = "VA", _("Valor")
    PORCENTAGEM = "PO", _("Porcentagem")

class RateioCentroDeCusto(models.Model):
    movimentacao = models.ForeignKey("financeiro.Movimentacao", related_name="rateios", on_delete=models.CASCADE)
    centro_de_custo = models.ForeignKey(CentroDeCusto, verbose_name="Centro de Custo", on_delete=models.PROTECT)
    tipo_rateio = models.CharField(
        max_length=2,
        choices=TipoRateio.choices,
        default=TipoRateio.VALOR,
        verbose_name="Tipo de Rateio"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def clean(self):
        super().clean()
        if self.tipo_rateio == TipoRateio.VALOR and self.valor is None:
            raise ValidationError("Para o tipo de rateio por valor, o campo 'valor' deve ser preenchido.")
        elif self.tipo_rateio == TipoRateio.PORCENTAGEM and self.percentual is None:
            raise ValidationError("Para o tipo de rateio por porcentagem, o campo 'percentual' deve ser preenchido.")
        
    def __str__(self):
        return f"{self.movimentacao} - {self.centro_de_custo}"
    
    def validar_rateio_total(self,movimentacao):
        total_percentual = self.objects.filter(movimentacao=movimentacao).aggregate(Sum("percentual"))["total"] or 0

        if total_percentual > 100:
            raise ValidationError(_("A soma dos rateios por porcentagem não pode ultrapassar 100%."))