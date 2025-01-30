from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from operacoes.models import NaturezaFinanceira, CentroDeCusto
from cadastro.models import Cadastro
from bancos.models import ContaBancaria
from simple_history.models import HistoricalRecords


class TipoMovimentacao(models.TextChoices):
    RECEITA = "RE", "Receita"
    DESPESA = "DE", "Despesa"
    

class FormaRecebimento(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
    tipo_movimentacao = models.CharField(
        max_length=2,
        choices=TipoMovimentacao.choices,
        verbose_name="Tipo de Movimentação"
    )
    natureza_financeira = models.ForeignKey(NaturezaFinanceira, verbose_name="Natureza Financeira", on_delete=models.PROTECT)
    centro_de_custo = models.ForeignKey(CentroDeCusto, verbose_name="Centro de Custo", on_delete=models.PROTECT)
    data_movimentacao = models.DateField(verbose_name="Data Movimentação", default=timezone.now)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    parcelado = models.BooleanField(default=False, verbose_name="Parcelado")
    total_parcelas = models.PositiveIntegerField(
        null=True, blank=True, 
        verbose_name="Total de Parcelas",
        help_text="Informe o número total de parcelas se a movimentação for parcelada."
    )
    forma_recebimento = models.ForeignKey(FormaRecebimento, on_delete=models.PROTECT)
    data_vencimento = models.DateField()
    cadastro = models.ForeignKey(Cadastro, verbose_name="Cliente/Fornecedor", on_delete=models.PROTECT)
    conta_bancaria = models.ForeignKey(ContaBancaria, verbose_name="Conta Bancária", on_delete=models.PROTECT)
    pago = models.BooleanField(default=False, verbose_name="Pago")
    historico = HistoricalRecords(
        excluded_fields=['parcelas', 'rateios'],
        history_change_reason_field=models.TextField(null=True)
    )

    def __str__(self):
        return f"{self.descricao} - {self.get_tipo_movimentacao_display()} - R$ {self.valor:.2f}"

    def atualizar_status_pagamento(self):
        """
        Atualiza o status 'pago' da movimentação principal.
        Será marcado como 'pago' apenas se TODAS as parcelas forem pagas.
        """
        if self.parcelado:
            todas_pagaram = self.parcelas.filter(pago=False).count() == 0
            self.pago = todas_pagaram
        self.save(update_fields=['pago'])

    def clean(self):
        super().clean()

        if self.parcelado and not self.total_parcelas:
            raise ValidationError("Você deve informar o número total de parcelas para movimentações parceladas.")

        if self.parcelado and self.total_parcelas < 2:
            raise ValidationError("O número de parcelas deve ser no mínimo 2.")

        if self.pk and self.rateios.exists():
            total_percentual = sum(rateio.percentual or 0 for rateio in self.rateios.all() if rateio.tipo_rateio == TipoRateio.PORCENTAGEM)
            if total_percentual > 100:
                raise ValidationError("A soma dos percentuais do rateio não pode ultrapassar 100%.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica se a movimentação é nova
        old_pago = None

        if not is_new:
            old_instance = Movimentacao.objects.get(pk=self.pk)
            old_pago = old_instance.pago

        super().save(*args, **kwargs)

        # 📌 GARANTIR QUE AS PARCELAS SÓ SEJAM GERADAS UMA VEZ
        if self.parcelado and not self.parcelas.exists():
            self.gerar_parcelas()

        # 📌 ATUALIZAÇÃO DO SALDO SE O STATUS "PAGO" MUDOU
        if old_pago is not None and old_pago != self.pago:
            self.conta_bancaria.atualizar_saldo(valor=self.valor, adicionar=(self.tipo_movimentacao == TipoMovimentacao.RECEITA))


    def gerar_parcelas(self):
        self.parcelas.all().delete()
        valor_parcela = round(self.valor / self.total_parcelas, 2)

        for i in range(1, self.total_parcelas + 1):
            Parcela.objects.create(
                movimentacao=self,
                numero=i,
                valor=valor_parcela,
                data_vencimento=self.data_vencimento + relativedelta(months=i - 1)
            )

    def atualizar_saldo(self, conta, valor, adicionar):
        if adicionar:
            conta.saldo_atual += valor
        else:
            conta.saldo_atual -= valor
        conta.save()

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"


class TipoRateio(models.TextChoices):
    VALOR = "VA", "Valor"
    PORCENTAGEM = "PO", "Porcentagem"


class RateioCentroDeCusto(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, related_name="rateios", on_delete=models.CASCADE)
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


class Parcela(models.Model):
    movimentacao = models.ForeignKey(Movimentacao, related_name="parcelas", on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(verbose_name="Número da Parcela")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False, verbose_name="Pago")
    data_vencimento = models.DateField()

    def __str__(self):
        return f"Parcela {self.numero} - R$ {self.valor:.2f}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_pago = None

        if not is_new:
            old_instance = Parcela.objects.get(pk=self.pk)
            old_pago = old_instance.pago

        super().save(*args, **kwargs)

        if old_pago is not None and old_pago != self.pago:
            self.movimentacao.conta_bancaria.atualizar_saldo(
                valor=self.valor,
                adicionar=(self.movimentacao.tipo_movimentacao == TipoMovimentacao.RECEITA if self.pago else self.movimentacao.tipo_movimentacao == TipoMovimentacao.DESPESA)
            )

        self.movimentacao.atualizar_status_pagamento()

    class Meta:
        unique_together = ('movimentacao', 'numero')
