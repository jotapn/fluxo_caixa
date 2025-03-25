from cadastro.models import Pessoa
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField()
    ativo = models.BooleanField(default=True)
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete= models.SET_NULL,
        blank=True,
        null =True,
        related_name="usuario"
    )

    def __str(self):
        return self.username