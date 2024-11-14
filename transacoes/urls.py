from django.urls import path
from .views import (
    EntradaListView, EntradaDetailView, EntradaCreateView, EntradaUpdateView, EntradaDeleteView,
    SaidaListView, SaidaDetailView, SaidaCreateView, SaidaUpdateView, SaidaDeleteView, DashboardView
)

from . import views


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Tela inicial

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

    path('importar/entradas/', views.importar_entradas_view, name='importar_entradas'),
    path('importar/saidas/', views.importar_saidas_view, name='importar_saidas'),
    path('sucesso/', views.SucessoView.as_view(), name='sucesso'),
]