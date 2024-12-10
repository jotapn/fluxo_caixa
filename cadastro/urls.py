from django.urls import path
from .views import criar_cadastro, CadastroListView

urlpatterns = [
    path('', CadastroListView.as_view(), name='listar-cadastro'),
    path('criar', criar_cadastro, name='criar-cadastro'),
]
