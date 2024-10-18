from django.db import models

class Cliente(models.Model):
    PESSOA =(
        ('pf', "Pessoa física"),
        ('pj', "Pessoa jurídica"),
    )
    nome_fantasia = models.CharField(max_length=80)
    razao_social = models.CharField(max_length=80)
    tipo_pessoa = models.CharField(max_length=20,choices=PESSOA, null=True, blank=True)
    cnpj_cpf = models.CharField(max_length=18)
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=6)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome_fantasia