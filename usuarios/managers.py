from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Gerenciador de usuários customizado que usa username ao invés de e-mail.
    """
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("O campo username é obrigatório")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_login", False)

        return self.create_user(username, password, **extra_fields)
