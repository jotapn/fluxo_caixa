import django.shortcuts
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from movimentacoes.models import Entrada, Saida
from .models import Banco, ContaBancaria
from .forms import BancoModelForm, ContaBancariaModelForm


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
        
class ContaBancariaListView(ListView):
    '''LISTAGEM DE CONTAS BANCÁRIAS'''
    model = ContaBancaria
    template_name = 'conta_bancaria_list.html'
    context_object_name = 'contas'
    
class ContaBancariaCreateView(CreateView):
    '''CRIAÇÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    form_class = ContaBancariaModelForm
    template_name = 'conta_bancaria_form.html'
    success_url = reverse_lazy('conta_bancaria_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'AT'  # Define o status como ativo por padrão
        return initial

class ContaBancariaDetailView(DetailView):
    '''DETALHAMENTO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    template_name = 'conta_bancaria_detail.html'
    context_object_name = 'conta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pegar as movimentações (entradas e saídas) da conta bancária atual
        conta = self.get_object()
        entradas = Entrada.objects.filter(conta=conta)
        saidas = Saida.objects.filter(conta=conta)

        # Combinar e ordenar por data
        movimentacoes = sorted(
            list(entradas) + list(saidas),
            key=lambda mov: mov.data,
            reverse=True
        )

        context['movimentacoes'] = movimentacoes
        return context

class ContaBancariaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    form_class = ContaBancariaModelForm
    template_name = 'conta_bancaria_form.html'
    success_url = reverse_lazy('conta_bancaria_list')

    def form_valid(self, form):
        cb = self.get_object()
        saldo_inicial_antigo = cb.saldo_inicial
        nova_cb = form.save(commit=False)

        if saldo_inicial_antigo != nova_cb.saldo_inicial:
            form.add_error('saldo_inicial', "Não é permitido alterar o saldo inicial de uma conta já cadastrada.")
            return self.form_invalid(form)
        
        nova_cb.save()
        return super().form_valid(form)
    

class ContaBancariaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    template_name = 'conta_bancaria_confirm_delete.html'
    success_url = reverse_lazy('conta_bancaria_list')