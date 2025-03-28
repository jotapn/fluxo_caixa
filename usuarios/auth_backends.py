from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        # Permitir login tanto com username quanto com email
        if username:
            user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()

        if user and user.check_password(password):
            # Verificar se o usuário está ativo
            if not user.ativo:
                raise PermissionDenied("Usuário ou senha inválidos.")  # Simula erro de credenciais inválidas

            # Impedir login se for o primeiro acesso sem troca de senha
            if user.first_login:
                raise PermissionDenied("Você deve alterar sua senha antes de continuar.")

            return user  # Retorna o usuário autenticado
        
        return PermissionDenied("Usuário ou senha inválidos.")  # Retorna None para login inválido
    
