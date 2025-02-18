from django.db import models
from validate_docbr import CPF, CNPJ
from django.core.exceptions import ValidationError
import brazilcep

class TipoEndereco(models.TextChoices):
    PRINCIPAL = "PR", "Principal"
    COBRANCA = "CO", "Cobrança"

class TipoPessoa(models.TextChoices):
    FISICA = "PF", "Pessoa Física"
    JURIDICA = "PJ", "Pessoa Jurídica"
    ESTRANGEIRO = "ET", "Estrangeiro"

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

def validar_cpf_cnpj(value):
    if len(value) == 14:
        if not CPF().validate(value):
            raise ValidationError("CPF inválido")
    elif len(value) == 18:
        if not CNPJ().validate(value):
            raise ValidationError("CNPJ inválido")
    return True

class Pessoa(BaseModel):
    tipo_pessoa = models.CharField(max_length=2, choices=TipoPessoa.choices)
    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=80, null=True, blank=True, verbose_name="Nome Fantasia")
    cnpj_cpf = models.CharField(max_length=18, unique=True, validators=[validar_cpf_cnpj], blank=True, null=True)
    atributos = models.ManyToManyField(Atributo, related_name="pessoas")
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.nome}"

    def endereco_principal(self):
        """Retorna o endereço principal associado ao cadastro."""
        return self.enderecos.filter(tipo=TipoEndereco.PRINCIPAL).first()
    
    def clean(self):
        super().clean()
        if self.tipo_pessoa == "PJ" and not self.nome_fantasia:
            raise ValidationError({"nome_fantasia": "O campo Nome Fantasia é obrigatório para Pessoas Jurídicas."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

def valida_cep(value):
    if not brazilcep.get_address_from_cep(value):
        raise("CEP inválido")

class Endereco(models.Model):
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="enderecos",
    )
    
    tipo = models.CharField(
        max_length=2,
        choices=TipoEndereco.choices,
        default=TipoEndereco.PRINCIPAL
    )

    cep = models.CharField(max_length=9,validators=[valida_cep])
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
    
    class Meta:
        constraints = [
            # Restringe um único endereço principal por cadastro
            models.UniqueConstraint(
                fields=["pessoa", "tipo"],
                condition=models.Q(tipo=TipoEndereco.PRINCIPAL),
                name="unique_principal_endereco_per_pessoa"
            )
        ]