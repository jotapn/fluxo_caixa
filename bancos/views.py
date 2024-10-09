from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from .models import Banco, ContaBancaria
from .forms import BancoModelForm


##### CRUD DE BANCOS ######
class BancoCreateView(CreateView):
    '''CRIAÇÃO DE UM NOVO BANCO'''
    model = Banco
    form_class = BancoModelForm
    template_name = 'banco_form.html'
    success_url = reverse_lazy('banco-list')


class BancoListView(ListView):
    '''LISTAGEM DOS BANCOS'''
    model = Banco
    template_name = 'banco_list.html'
    context_object_name = 'bancos'


class BancoDetailView(DetailView):
    '''DETALHAMENTO DE UM BANCO'''
    model = Banco
    template_name = 'banco_detail.html'
    context_object_name = 'banco'


class BancoUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM BANCO'''
    model = Banco
    template_name = 'banco_form.html'
    form_class = BancoModelForm
    success_url = reverse_lazy('banco-list')

class ContaBancariaUpdateView(UpdateView):

    model = ContaBancaria
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValueError as e:
            form.add_error('saldo_inicial', str(e))  # Adiciona erro ao campo de saldo inicial
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Banco'
        return context


class BancoDeleteView(DeleteView):
    '''EXCLUSÃO DE UM BANCO'''
    model = Banco
    template_name = 'banco_confirm_delete.html'
    success_url = reverse_lazy('banco-list')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Não é possível excluir este banco porque ele está relacionado a contas ativas.")
            return self.get(request, *args, **kwargs)