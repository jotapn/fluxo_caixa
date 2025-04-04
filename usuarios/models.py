from cadastro.models import Pessoa
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ativo = models.BooleanField(default=True)
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete= models.SET_NULL,
        blank=True,
        null =True,
        related_name="usuario_pessoa"
    )
    first_login = models.BooleanField(default=True)  # Indica se o usuário deve alterar a senha
    objects = CustomUserManager()

    @property
    def email(self):
        return self.pessoa.email if self.pessoa else None
    
    @email.setter
    def email(self, value):
        pass

    def __str__(self):
        return self.username