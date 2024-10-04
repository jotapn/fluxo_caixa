from django.urls import path
from .views import (
    BancoListView, BancoDetailView, BancoCreateView, BancoUpdateView, BancoDeleteView,
    TipoListView, TipoDetailView, TipoCreateView, TipoUpdateView, TipoDeleteView,
    EntradaListView, EntradaDetailView, EntradaCreateView, EntradaUpdateView, EntradaDeleteView,
    SaidaListView, SaidaDetailView, SaidaCreateView, SaidaUpdateView, SaidaDeleteView, MovimentacaoListView
)


urlpatterns = [
    path("", MovimentacaoListView.as_view(), name="movimentacoes_list"),

    # URLs de Banco
    path('bancos/', BancoListView.as_view(), name='banco-list'),
    path('bancos/<int:pk>/', BancoDetailView.as_view(), name='banco-detail'),
    path('bancos/novo/', BancoCreateView.as_view(), name='banco-create'),
    path('bancos/editar/<int:pk>/', BancoUpdateView.as_view(), name='banco-update'),
    path('bancos/<int:pk>/deletar/', BancoDeleteView.as_view(), name='banco-delete'),

    # URLs de Tipo
    path('tipos/', TipoListView.as_view(), name='tipo-list'),
    path('tipos/<int:pk>/', TipoDetailView.as_view(), name='tipo-detail'),
    path('tipos/novo/', TipoCreateView.as_view(), name='tipo-create'),
    path('tipos/<int:pk>/editar/', TipoUpdateView.as_view(), name='tipo-update'),
    path('tipos/<int:pk>/deletar/', TipoDeleteView.as_view(), name='tipo-delete'),

    # URLs de Entrada
    path('entradas/', EntradaListView.as_view(), name='entrada-list'),
    path('entradas/<int:pk>/', EntradaDetailView.as_view(), name='entrada-detail'),
    path('entradas/nova/', EntradaCreateView.as_view(), name='entrada-create'),
    path('entradas/<int:pk>/editar/', EntradaUpdateView.as_view(), name='entrada-update'),
    path('entradas/<int:pk>/deletar/', EntradaDeleteView.as_view(), name='entrada-delete'),

    # URLs de Saida
    path('saidas/', SaidaListView.as_view(), name='saida-list'),
    path('saidas/<int:pk>/', SaidaDetailView.as_view(), name='saida-detail'),
    path('saidas/nova/', SaidaCreateView.as_view(), name='saida-create'),
    path('saidas/<int:pk>/editar/', SaidaUpdateView.as_view(), name='saida-update'),
    path('saidas/<int:pk>/deletar/', SaidaDeleteView.as_view(), name='saida-delete'),
]