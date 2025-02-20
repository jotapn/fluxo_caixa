from django.urls import path
from .views import criar_pessoa, PessoaListView

urlpatterns = [
    path('', PessoaListView.as_view(), name='listar-pessoa'),
    path('criar', criar_pessoa, name='criar-pessoa'),
]
