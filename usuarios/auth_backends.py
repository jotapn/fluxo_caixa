from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(username=username).first()

        # Permitir login tanto com username quanto com email
        if not user:
            user = User.objects.filter(pessoa__email=username).first()

        if not user:
            return None
        
        if not user.check_password(password):
            return None

        # Bloqueia login de usuários inativos
        if not user.ativo:
            raise PermissionDenied("Usuário ou senha inválidos.")  # Mensagem genérica de erro

        # Se for primeiro login, forçar alteração de senha
        if user.first_login:
            raise PermissionDenied("Você deve alterar sua senha antes de continuar.")

        return user  # Retorna o usuário autenticado
    