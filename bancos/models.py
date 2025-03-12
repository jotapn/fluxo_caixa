from django.db import models
from django.db.models import Sum, Case, When, F, Value, DecimalField

class Banco(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Banco")
    logo = models.ImageField(upload_to="bancos/logos/", null=True, blank=True, verbose_name="Logo do Banco")
    status = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.nome}"

class ContaBancaria(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    cartao_credito = models.BooleanField(default=False)
    descricao = models.CharField(max_length=50)
    conta = models.CharField(max_length=20)
    agencia = models.CharField(max_length=20, verbose_name='Agência')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.BooleanField(default=True, verbose_name="Ativo")
    
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