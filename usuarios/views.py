from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    print("View logout")
    # permission_classes = [permissions.IsAuthenticated]
    print("View logout - permissao")

    def post(self,request):
        try:
            refresh_token = request.data.get("refresh")
            print(f"pegou o refresh {refresh_token}")
            token = RefreshToken(refresh_token)
            print(f"pegou o token {token}")
            token.blacklist()

            return Response({"message": "Logout realizado com sucesso"}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"error": "Token inválido ou já expirado."}, status=status.HTTP_400_BAD_REQUEST)