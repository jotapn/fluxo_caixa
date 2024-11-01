from django.db import models

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
    nome = models.CharField(max_length=50)
    conta = models.CharField(max_length=20)
    agencia = models.CharField(max_length=20, verbose_name='Agência')
    gerente = models.CharField(max_length=200, null=True, blank=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_atual = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True,auto_created=True, default=0)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ATIVO)

    @property
    def saldo_atual_formatado(self):
        return f"R$ {self.saldo_atual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def saldo_inicial_formatado(self):
        return f"R$ {self.saldo_inicial:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def status_formatado(self):
        return self.get_status_display()
        
    def __str__(self) -> str:
        return self.nome