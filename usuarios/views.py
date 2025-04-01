from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import logout, login
from .serializers import LoginSerializer

class LoginView(APIView):
    """
    Autentica um usuário e retorna uma resposta com o token de sessão.
    """
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({'message': "Login realizado com sucesso"}, status= status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self,request):
        request.auth.delete()
        logout(request)
        return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)