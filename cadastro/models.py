from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.exceptions import ValidationError
from validate_docbr import CPF, CNPJ
import brazilcep


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Atributos(models.TextChoices):
    CLIENTE = "CL", "Cliente"
    FORNECEDOR = "FO", "Fornecedor"
    COLABORADOR = "CO", "Colaborador"

class TipoPessoa(models.TextChoices):
    FISICA = "PF", "Pessoa Física"
    JURIDICA = "PJ", "Pessoa Jurídica"
    ESTRANGEIRO = "ET", "Estrangeiro"

class Pessoa(BaseModel):
    tipo_pessoa = models.CharField(max_length=2, choices=TipoPessoa.choices)
    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=80, null=True, blank=True, verbose_name="Nome Fantasia")
    cnpj_cpf = models.CharField(max_length=18, unique=True, blank=True, null=True)
    atributos = ArrayField(
        models.CharField(max_length=2, choices=Atributos.choices),
        blank=True,
        default=list
    )
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.nome}"
    
    @classmethod
    def colaboradores_sem_usuario(cls):
        return cls.objects.filter(atributos__contains=['CO']).filter(usuario__isnull=True)
    
    def get_atributos_display(self):
        return ", ".join([Atributos(atributo).label for atributo in self.atributos]) if self.atributos else "Nenhum"
    
    get_atributos_display.short_description = "Atributos"

    def clean_cpf_cnpj(self):
        if not self.cnpj_cpf:
            return

        if self.tipo_pessoa == "PF":
            if not CPF().validate(self.cnpj_cpf):
                raise ValidationError("CPF inválido")
        elif self.tipo_pessoa == 'PJ':
            if not CNPJ().validate(self.cnpj_cpf):
                raise ValidationError("CNPJ inválido")
    
    def clean(self):
        super().clean()
        if self.tipo_pessoa == "PJ" and not self.nome_fantasia:
            raise ValidationError({"nome_fantasia": "O campo Nome Fantasia é obrigatório para Pessoas Jurídicas."})

    def save(self, *args, **kwargs):
        self.full_clean()
        self.clean_cpf_cnpj()
        super().save(*args, **kwargs)

def valida_cep(value):
    endereco = brazilcep.get_address_from_cep(value)
    if not endereco:
        raise ValidationError("CEP inválido")

class Endereco(models.Model):
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="enderecos",
        null=True,
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
    principal = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero}, {self.municipio} - {self.estado}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pessoa'], condition=models.Q(principal=True), name='unique_principal_endereco')
        ]