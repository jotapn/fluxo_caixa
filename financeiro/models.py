from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from operacoes.models import NaturezaFinanceira, CentroDeCusto
from cadastro.models import Pessoa
from bancos.models import ContaBancaria
from simple_history.models import HistoricalRecords


class CondicaoPagamento(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    numero_parcelas = models.PositiveIntegerField(default=1)  # Usuário define quantas parcelas
    juros = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.numero_parcelas}x"

class FormaRecebimento(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class TipoMovimentacao(models.TextChoices):
    RECEITA = "RE", "Receita"
    DESPESA = "DE", "Despesa"

class Movimentacao(models.Model):
    tipo_movimentacao = models.CharField(max_length=2, choices=TipoMovimentacao.choices)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    condicao_pagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.PROTECT)
    natureza_financeira = models.ForeignKey(NaturezaFinanceira, on_delete=models.PROTECT)
    centro_de_custo = models.ForeignKey(CentroDeCusto, on_delete=models.PROTECT)
    data_movimentacao = models.DateField(default=timezone.now)
    forma_recebimento = models.ForeignKey(FormaRecebimento, on_delete=models.PROTECT)
    data_vencimento = models.DateField()
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)
    conta_bancaria = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)

    historico = HistoricalRecords()

    def __str__(self):
        return f"{self.descricao} - {self.get_tipo_movimentacao_display()} - R$ {self.valor:.2f}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # ✅ Primeiro salva a movimentação para garantir um ID

        if is_new:  
            self.gerar_parcelas()  # 📌 Gera automaticamente as parcelas na criação

    def gerar_parcelas(self):
        """ Gera as parcelas aplicando juros automaticamente """
        self.parcelas.all().delete()  # Remove parcelas anteriores caso existam

        # 📌 Calculando o valor total com juros
        valor_total = self.valor * (1 + (self.condicao_pagamento.juros))
        valor_parcela = round(valor_total / self.condicao_pagamento.numero_parcelas, 2)

        for i in range(1, self.condicao_pagamento.numero_parcelas + 1):
            Parcela.objects.create(
                movimentacao=self,
                numero=i,
                valor=valor_parcela,  # ✅ Agora o valor da parcela inclui os juros
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
        saldo_anterior = self.movimentacao.conta_bancaria.saldo_atual

        if not is_new:
            old_instance = Parcela.objects.get(pk=self.pk)
            old_pago = old_instance.pago  # ✅ Captura o status anterior de pagamento

        super().save(*args, **kwargs)

        if old_pago is not None and old_pago != self.pago:
            adicionar = self.pago if self.movimentacao.tipo_movimentacao == TipoMovimentacao.RECEITA else not self.pago

            self.movimentacao.conta_bancaria.atualizar_saldo(
                valor=self.valor,
                adicionar=adicionar
            )

            saldo_posterior = self.movimentacao.conta_bancaria.saldo_atual

            HistoricoTransacao.objects.create(
                transacao=self.movimentacao,
                data_movimentacao=timezone.now(),
                tipo_movimentacao=self.movimentacao.tipo_movimentacao,
                valor=self.valor,
                saldo_anterior=saldo_anterior,
                saldo_posterior=saldo_posterior,
                conta_bancaria=self.movimentacao.conta_bancaria,
            )

class HistoricoTransacao(models.Model):
    transacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE,related_name="historico_transacao")
    data_movimentacao = models.DateField(auto_now=True)
    tipo_movimentacao = models.CharField(choices=TipoMovimentacao.choices, max_length=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_posterior = models.DecimalField(max_digits=10, decimal_places=2)
    conta_bancaria = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.get_tipo_movimentacao_display()} - R$ {self.valor:.2f} ({self.data_movimentacao})"