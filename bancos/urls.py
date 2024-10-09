from django.urls import path
from .views import (
    BancoListView, BancoDetailView, BancoCreateView, BancoUpdateView, BancoDeleteView, ContaBancariaListView, ContaBancariaCreateView, ContaBancariaUpdateView, ContaBancariaDeleteView, ContaBancariaDetailView
)

urlpatterns = [
    path('bancos/', BancoListView.as_view(), name='banco-list'),
    path('bancos/<int:pk>/', BancoDetailView.as_view(), name='banco-detail'),
    path('bancos/novo/', BancoCreateView.as_view(), name='banco-create'),
    path('bancos/editar/<int:pk>/', BancoUpdateView.as_view(), name='banco-update'),
    path('bancos/<int:pk>/deletar/', BancoDeleteView.as_view(), name='banco-delete'),

    path('contas/', ContaBancariaListView.as_view(), name='conta_bancaria_list'),
    path('contas/criar/', ContaBancariaCreateView.as_view(), name='conta_bancaria_create'),
    path('contas/<int:pk>/', ContaBancariaDetailView.as_view(), name='conta_bancaria_detail'),
    path('contas/<int:pk>/editar/', ContaBancariaUpdateView.as_view(), name='conta_bancaria_update'),
    path('contas/<int:pk>/excluir/', ContaBancariaDeleteView.as_view(), name='conta_bancaria_delete'),
]