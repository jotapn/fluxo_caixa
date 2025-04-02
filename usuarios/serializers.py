from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Permite login com username ou email e adiciona mais informações na resposta do token.
    """

    def validate(self, attrs):
        username_or_email = attrs.get("username")  # O campo no SimpleJWT ainda se chama "username"
        password = attrs.get("password")

        # Verifica se o usuário digitou um e-mail ou um username
        user = User.objects.filter(username=username_or_email).first()

        if not user:
            user = User.objects.filter(pessoa__email=username_or_email).first()

        if user is None:
            raise serializers.ValidationError({"error": "Usuário ou senha inválidos."})

        # Autentica o usuário com username (mesmo se encontrou pelo email)
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is None:
            raise serializers.ValidationError({"error": "Usuário ou senha inválidos."})

        if not authenticated_user.ativo:
            raise serializers.ValidationError({"error": "Usuário inativo. Entre em contato com o suporte."})

        # Se passou por todas as validações, gera os tokens
        data = super().validate({"username": user.username, "password": password})

        # Adicionamos informações personalizadas ao response do login
        data.update({
            "user_id": authenticated_user.id,
            "username": authenticated_user.username,
            "email": authenticated_user.pessoa.email if authenticated_user.pessoa else None,
            "is_staff": authenticated_user.is_staff,
            "is_superuser": authenticated_user.is_superuser,
            "pessoa_id": authenticated_user.pessoa.id if authenticated_user.pessoa else None,
        })

        return data
