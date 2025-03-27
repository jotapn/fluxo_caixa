from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()

class CustomUserBackend(ModelBackend):

    def authenticate(self, request, username =None, password = None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)

        if user and not user.ativo:
            raise PermissionDenied("Usuário ou senha inválidos.") 
        # Faz o Django tratar como login incorreto
        if user.first_login:
            raise PermissionDenied("Você deve alterar sua senha antes de continuar.")
        
        return user