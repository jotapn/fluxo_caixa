from django.db import models
from django.db import transaction
from bancos.models import ContaBancaria
from clientes.models import Cliente
from operacoes.models import TipoReceita, TipoDespesa, TipoPagamento

SITUACAO = (
    ("PG", "Pago"),
    ("AP", "A pagar")
)


class Entrada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    conta = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    tipo_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.PROTECT, related_name='pagamentos')
    tipo_receita = models.ForeignKey(TipoReceita, on_delete=models.PROTECT, related_name='receitas', null=True)
    situacao = models.CharField(max_length=2, choices=SITUACAO, default='AP')

    def __str__(self):
        return f'Entrada: {self.valor} - {self.descricao}'
    
    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def situacao_formatado(self):
        for sigla, descricao in SITUACAO:
            if self.situacao == sigla:
                return descricao
        return self.situacao  # Retorna a sigla se não encontrar
    
    class Meta:
        ordering= ['-data']


class Saida(models.Model):
    tipo_despesa = models.ForeignKey(TipoDespesa, on_delete=models.PROTECT,related_name='despesas_saida')
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    conta = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT, null=True, blank=True)
    tipo_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.PROTECT, related_name='saidas')
    situacao = models.CharField(max_length=2, choices=SITUACAO, default='AP')

    def __str__(self):
        return f'Saída: {self.valor} - {self.descricao}'
    
    # def save(self, *args, **kwargs):
    #     # Verifica se a saída é nova (ou seja, ainda não tem um ID) ou se a situação mudou para 'Pago'
    #     if self.pk is None or Saida.objects.get(pk=self.pk).situacao != 'PG':
    #         # Se a situação é "PG" (Pago), diminui o valor no saldo atual da conta
    #         if self.situacao == 'PG':
    #             self.conta.saldo_atual -= self.valor
    #             self.conta.save()
        
    #     super(Saida, self).save(*args, **kwargs)
    
    # def delete(self, *args, **kwargs):
    #     with transaction.atomic():
    #         # Primeiro, buscar a saída para saber o valor a ser adicionado ao saldo
    #         valor = self.valor
    #         super().delete(*args, **kwargs)  # Excluir a entrada

    #         # Atualizar o saldo da conta bancária associada
    #         conta = self.conta
    #         conta.saldo_atual += valor
    #         conta.save()

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def situacao_formatado(self):
        for sigla, descricao in SITUACAO:
            if self.situacao == sigla:
                return descricao
        return self.situacao  # Retorna a sigla se não encontrar
    
    class Meta:
        ordering= ['-data']