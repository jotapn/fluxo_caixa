from cadastro.models import Pessoa
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete= models.SET_NULL,
        blank=True,
        null =True,
        related_name="usuario_pessoa"
    )

    def __str__(self):
        return self.username