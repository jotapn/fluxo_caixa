from django.db import models
from bancos.models import ContaBancaria
from cadastro.models import Cadastro
from django.utils import timezone


class CentroDeCusto(models.Model):
    codigo = models.CharField(max_length=8, unique=True) 
    nome = models.CharField(max_length=50) 
    descricao = models.TextField(null=True, blank=True) 
    ativo = models.BooleanField(default=True)
    pai = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="sub_centros"
    )  

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class NaturezaFinanceira(models.Model):
    codigo = models.CharField(max_length=20, unique=True)  
    nome = models.CharField(max_length=50)  #
    descricao = models.TextField(null=True, blank=True)  
    sinal = models.CharField(
        max_length=2,
        choices=[
            ("DE", "Débito"),  
            ("CR", "Crédito"),  
            ("TR", "Transitório"),  
        ],
    )  
    ativo = models.BooleanField(default=True)  
    pai = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="sub_naturezas"
    )  

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
class OperacaoFinanceira(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField(default=timezone.now)
    conta = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    natureza_financeira = models.ForeignKey(NaturezaFinanceira, on_delete=models.PROTECT, related_name='operacao_natureza')
        #DEPOIS VERIFICAR:  QUANDO A NATUREZA FOR COM SINAL CRÉDITO: SUBTRAI VALOR /// QUANDO A NATUREZA COM SINAL DÉBITO: ADICIONA VALOR A CONTA /// QUANDO TRANSITÓRIO: REMOVE DA CONTA ORIGEM E ADC NA CONTA DESTINO 
    centro_de_custo = models.ForeignKey(CentroDeCusto, on_delete=models.PROTECT, related_name='operacao_centro' )
        #DEPOIS VERIFICAR: PODER RATEAR CENTRO DE CUSTO
    pessoa = models.ForeignKey(Cadastro, on_delete=models.PROTECT, related_name='operacao_pessoa' )
        #DEPOIS VERIFICAR: LISTAR PESSOAS COM ATRIBUTO CLIENTE QUANDO NATUREZA DE DÉBITO E LISTAR PESSOA COM ATRIBUTO FORNECEDOR QUANDO NATUREZA CRÉDITO
    pago = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_vencimento']

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def situacao_formatado(self):
        if self.natureza_financeira.sinal == "DE":
            if self.pago == False:
                return "A receber"
            return "Recebido"
        else:
            if self.pago == False:
                return "A pagar"
            return "Pago"
        
            