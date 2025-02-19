from django.db import models
from django.core.exceptions import ValidationError
from cadastro.models import Pessoa, Atributo, Atributos

class CentroDeCusto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=50)
    responsavel = models.ForeignKey(Pessoa, null=True, blank=True,on_delete=models.PROTECT,
        limit_choices_to={
            "atributos__tipo": Atributos.COLABORADOR
            },
        )

    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        if self.responsavel and not self.responsavel.atributos.filter(tipo=Atributos.COLABORADOR).exists():
            raise ValidationError("O responsável deve ser um cadastro com o atributo de Colaborador.")
        
    def __str__(self):
        return self.titulo
        
class TipoNatureza(models.TextChoices):
    SINTETICA = "ST", "Sintética"
    #GERAL, MAIOR HIERARQUIA
    ANALITICA = "AN", "Analítica"
    #MAIS DETALHADA, MENOR HIERARQUIA

class SinalNatureza(models.TextChoices):
    CREDITO = "CR", 'Crédito'
    #ENTRADA DE CAPITAL
    DEBITO = "DB", "Débito"
    #SAIDA DE CAPITAL
    TRANSITORIA = "TR", "Transitória"
    #TRANSFERENCIAS DE CAPITAL ENTRE CONTAS

class NaturezaFinanceira(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TipoNatureza.choices)
    sinal = models.CharField(max_length=2, choices=SinalNatureza.choices)
    grupo = models.ForeignKey("self", 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={
            "tipo": TipoNatureza.SINTETICA
            },
        )
    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        if self.tipo == TipoNatureza.ANALITICA and not self.grupo:
            raise ValidationError("Naturezas do tipo Analítica devem estar vinculadas a um grupo do tipo Sintética.")
        
        if self.grupo and self.grupo.tipo != TipoNatureza.SINTETICA:
            raise ValidationError("O grupo deve ser uma Natureza do tipo Sintética.")
        
        
    class Meta:
        verbose_name = "Natureza Financeira"
        verbose_name_plural = "Naturezas Financeiras"

    def __str__(self):
        return self.titulo