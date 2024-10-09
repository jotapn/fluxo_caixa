from django.urls import path
from .views import (
    BancoListView, BancoDetailView, BancoCreateView, BancoUpdateView, BancoDeleteView
)

urlpatterns = [
    path('bancos/', BancoListView.as_view(), name='banco-list'),
    path('bancos/<int:pk>/', BancoDetailView.as_view(), name='banco-detail'),
    path('bancos/novo/', BancoCreateView.as_view(), name='banco-create'),
    path('bancos/editar/<int:pk>/', BancoUpdateView.as_view(), name='banco-update'),
    path('bancos/<int:pk>/deletar/', BancoDeleteView.as_view(), name='banco-delete'),
]