from django.urls import path
from clientes.views import ClientesListView, ClienteCreateView, ClientesUpdateView, ClientesDeleteView

urlpatterns = [
    path("", ClientesListView.as_view(), name="clientes-list"),
    path("novo", ClienteCreateView.as_view(), name="clientes-create"),
    path("<int:pk>", ClientesUpdateView.as_view(), name="clientes-update"),
    path("delete/<int:pk>", ClientesDeleteView.as_view(), name="clientes-delete"),
]