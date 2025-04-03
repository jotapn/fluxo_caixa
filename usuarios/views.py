from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):

    permission_classes = []

    def post(self, request):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return Response({"error": "Usuário não autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"error": "Token de refresh não foi enviado."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Adiciona à blacklist

            return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Token inválido ou já expirado."}, status=status.HTTP_400_BAD_REQUEST)