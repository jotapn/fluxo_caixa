from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from clientes.models import Cliente
from . forms import ClienteModelForm

class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"
    context_object_name = 'clientes'

    def get_queryset(self):
        clientes = super().get_queryset().order_by('nome_fantasia')
        search = self.request.GET.get('search')
        if search:
            clientes = clientes.filter(model__icontains=search)
        return clientes
    
class ClienteCreateView(CreateView):
    model = Cliente
    template_name = "clientes_create.html"
    form_class = ClienteModelForm
    success_url = "/clientes/"

class ClientesUpdateView(UpdateView):
    model = Cliente
    template_name = "clientes_update.html"
    form_class = ClienteModelForm

    def get_success_url(self):
        return reverse_lazy('clientes_update', kwargs={'pk': self.object.pk})
    
class ClientesDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes_delete.html"
    success_url = "/clientes/"