from django.db import models
from django.db.models import Sum, Case, When, F, Value, DecimalField
from operacoes.models import NaturezaFinanceira

class Status(models.TextChoices):
    ATIVO = 'AT', "Ativo"
    INATIVO = 'IN', "Inativo"

class Banco(models.Model):
    nome = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ATIVO)

    @property
    def status_formatado(self):
        return self.get_status_display()

    def __str__(self):
        return self.nome

class ContaBancaria(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=50)
    conta = models.CharField(max_length=20)
    agencia = models.CharField(max_length=20, verbose_name='Agência')
    gerente = models.CharField(max_length=200, null=True, blank=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ATIVO)
    
    @property
    def status_formatado(self):
        return self.get_status_display()
        
    def __str__(self):
        return f"{self.descricao} - {self.banco.nome}"
    
    def calcular_saldo(self):
        saldo_movimentos = HistoricoSaldo.objects.filter(conta=self, movimentacao__pago=True).aggregate(
            total=Sum(
                Case(
                    When(movimentacao__natureza_financeira__sinal="CR", then=F("movimento")),  # Crédito → Soma
                    When(movimentacao__natureza_financeira__sinal="DB", then=-F("movimento")),  # Débito → Subtrai
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )["total"] or 0

        return self.saldo_inicial + saldo_movimentos


class HistoricoSaldo(models.Model):
    conta = models.ForeignKey(ContaBancaria, on_delete=models.CASCADE, related_name="historico")
    movimentacao = models.ForeignKey("financeiro.Movimentacao", on_delete=models.CASCADE, related_name="historico_saldo")
    data = models.DateTimeField(auto_now_add=True)
    movimento = models.DecimalField(max_digits=10, decimal_places=2)