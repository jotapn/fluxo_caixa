from django.db import models
from validate_docbr import CPF, CNPJ
from django.core.exceptions import ValidationError


class TipoPessoa(models.TextChoices):
    FISICA = "PF", "Pessoa Física"
    JURIDICA = "PJ", "Pessoa Jurídica"
    ESTRANGEIRO = "ET", "Estrangeiro"

def validar_cpf_cnpj(value):
    if len(value) <= 14:  # CPF
        if not CPF().validate(value):
            raise ValidationError("CPF inválido")
    else:  # CNPJ
        if not CNPJ().validate(value):
            raise ValidationError("CNPJ inválido")

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Atributos(models.TextChoices):
    CLIENTE = "CL", "Cliente"
    FORNECEDOR = "FO", "Fornecedor"
    COLABORADOR = "CO", "Colaborador"

class Atributo(models.Model):
    tipo = models.CharField(max_length=2, choices=Atributos.choices, unique=True)

    def __str__(self):
        return self.get_tipo_display()

class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=40, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.logradouro}, {self.numero}, {self.municipio} - {self.estado}"

class Cadastro(BaseModel):
    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=80)
    tipo_pessoa = models.CharField(max_length=2, choices=TipoPessoa.choices)
    cnpj_cpf = models.CharField(max_length=18, unique=True, validators=[validar_cpf_cnpj], blank=True, null=True)
    atributos = models.ManyToManyField(Atributo, related_name="cadastros")
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.nome}"
