from django.db import models

STATUS = (
    ("AT", "Ativo"),
    ("IN", "Inativo")
)

class Banco(models.Model):
    nome = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")

    @property
    def status_formatado(self):
        for id, descricao in STATUS:
            if self.status == id:
                return descricao
            return self.status

    def __str__(self):
        return self.nome

class ContaBancaria(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    nome = models.CharField(max_length=50)
    conta = models.CharField(max_length=20)
    agencia = models.CharField(max_length=20)
    gerente = models.CharField(max_length=200, null=True, blank=True)

    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_atual = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True,auto_created=True, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default="AT")

    @property
    def saldo_atual_formatado(self):
        return f"R$ {self.saldo_atual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def saldo_inicial_formatado(self):
        return f"R$ {self.saldo_inicial:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def status_formatado(self):
        for id, descricao in STATUS:
            if self.status == id:
                return descricao
            return self.status
        
    def __str__(self) -> str:
        return self.nome