from django.urls import path
from .views import ( OperacoesListView, CriarOperacaoView, TipoReceitaDetailView, TipoReceitaCreateView, TipoReceitaUpdateView, TipoReceitaDeleteView, TipoDespesaCreateView, TipoDespesaDeleteView, TipoDespesaDetailView, TipoDespesaUpdateView, TipoPagamentoCreateView, TipoPagamentoDetailView, TipoPagamentoUpdateView, TipoPagamentoDeleteView)

urlpatterns = [
    # URLs de Operacoes
    path('', OperacoesListView.as_view(), name='operacao-list'),

    path('criar/', CriarOperacaoView.as_view(), name='operacao-criar'),
    path('receita/criar/', TipoReceitaCreateView.as_view(), name='tipo_receita_create'),
    path('despesa/criar/', TipoDespesaCreateView.as_view(), name='tipo_despesa_create'),
    path('pagamento/criar/', TipoPagamentoCreateView.as_view(), name='tipo_pagamento_create'),
    
    path('receitas/<int:pk>/', TipoReceitaDetailView.as_view(), name='tipo_detail'),
    path('despesas/<int:pk>/', TipoDespesaDetailView.as_view(), name='tipo_detail'),
    path('pagamentos/<int:pk>/', TipoPagamentoDetailView.as_view(), name='tipo_detail'),
    
    path('receitas/<int:pk>/editar/', TipoReceitaUpdateView.as_view(), name='tipo_update'),
    path('despesas/<int:pk>/editar/', TipoDespesaUpdateView.as_view(), name='tipo_update'),
    path('pagamentos/<int:pk>/editar/', TipoPagamentoUpdateView.as_view(), name='tipo_update'),

    path('pagamentos/<int:pk>/deletar/', TipoPagamentoDeleteView.as_view(), name='tipo_delete'),
    path('despesas/<int:pk>/deletar/', TipoDespesaDeleteView.as_view(), name='tipo_delete'),
    path('receitas/<int:pk>/deletar/', TipoReceitaDeleteView.as_view(), name='tipo_delete'),
]