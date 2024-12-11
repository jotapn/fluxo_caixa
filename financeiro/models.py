from django.db import models

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
    titulo = models.CharField(max_length=50)  #
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
        return f"{self.codigo} - {self.titulo}"