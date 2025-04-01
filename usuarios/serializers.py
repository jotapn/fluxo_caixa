from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    print(f"🔍 Tentando autenticar: {username}")  # 👉 Depuração


    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            user = User.objects.filter(username=username).first()
            if user:
                user = authenticate(username=user.username, password=user.password)

        if not user or not isinstance(user, User):  # ⚠️ Corrigimos para evitar o erro
            print("❌ Falha na autenticação")  # 👉 Depuração
            raise serializers.ValidationError("Usuário ou senha inválidos.")
        
        if not getattr(user, "ativo", True):  # ⚠️ Usamos `getattr` para evitar erro caso user seja `None`
            print("⛔ Usuário inativo")  # 👉 Depuração
            raise PermissionDenied("Usuário inativo. Entre em contato com o suporte.")
        
        if getattr(user, "first_login", False):  # ⚠️ Usamos `getattr` para garantir segurança
            raise PermissionDenied("Você deve alterar sua senha antes de continuar.")
        
        print(f"✅ Login bem-sucedido: {user}")  # 👉 Depuração
        data['user'] = user
        return data