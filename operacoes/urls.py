from django.urls import path
from .views import ( OperacoesListView, TipoReceitaDetailView, TipoReceitaCreateView, TipoReceitaUpdateView, TipoReceitaDeleteView, TipoDespesaCreateView, TipoDespesaDeleteView, TipoDespesaDetailView, TipoDespesaUpdateView, TipoPagamentoCreateView, TipoPagamentoDetailView, TipoPagamentoUpdateView, TipoPagamentoDeleteView)

urlpatterns = [
    # URLs de Operacoes
    path('', OperacoesListView.as_view(), name='operacao-list'),

    # Receitas,
    path('receitas/novo/', TipoReceitaCreateView.as_view(), name='receita-create'),
    path('receitas/<int:pk>/', TipoReceitaDetailView.as_view(), name='receita-detail'),
    path('receitas/<int:pk>/editar/', TipoReceitaUpdateView.as_view(), name='receita-update'),
    path('receitas/<int:pk>/deletar/', TipoReceitaDeleteView.as_view(), name='receita-delete'),
    
    # Despesas
    path('despesas/novo/', TipoDespesaCreateView.as_view(), name='despesa-create'),
    path('despesas/<int:pk>/', TipoDespesaDetailView.as_view(), name='despesa-detail'),
    path('despesas/<int:pk>/editar/', TipoDespesaUpdateView.as_view(), name='despesa-update'),
    path('despesas/<int:pk>/deletar/', TipoDespesaDeleteView.as_view(), name='despesa-delete'),
    
    # Pagamentos
    path('pagamentos/novo/', TipoPagamentoCreateView.as_view(), name='pagamento-create'),
    path('pagamentos/<int:pk>/', TipoPagamentoDetailView.as_view(), name='pagamento-detail'),
    path('pagamentos/<int:pk>/editar/', TipoPagamentoUpdateView.as_view(), name='pagamento-update'),
    path('pagamentos/<int:pk>/deletar/', TipoPagamentoDeleteView.as_view(), name='pagamento-delete'),
]