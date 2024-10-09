from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .models import TipoReceita, TipoDespesa, TipoPagamento
from .forms import TipoDespesaModelForm, TipoPagamentoModelForm, TipoReceitaModelForm


class OperacoesListView(TemplateView):
    '''LISTAGEM DE OPERAÇÕES '''
    template_name = 'operacao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tipo_despesa = TipoDespesa.objects.all()
        tipo_receita = TipoReceita.objects.all()
        tipo_pagamento = TipoPagamento.objects.all()

        context['despesa'] = tipo_despesa
        context['receita'] = tipo_receita
        context['pagamento'] = tipo_pagamento

        return context



##### CRUD DE TIPOS DE RECEITA ######
class TipoReceitaCreateView(CreateView):
    '''CRIAÇÃO DE UM TIPO DE RECEITA'''
    model = TipoReceita
    template_name = 'operacao_form.html'
    form_class = TipoReceitaModelForm
    success_url = reverse_lazy('operacao-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'AT'  # Define o status como ativo por padrão
        return initial


class TipoReceitaDetailView(DetailView):
    '''DETALHAMENTO DE UM TIPO DE RECEITA'''
    model = TipoReceita
    template_name = 'receita/receita_detail.html'
    context_object_name = 'tipo'


class TipoReceitaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM TIPO'''
    model = TipoReceita
    template_name = 'operacao_form.html'
    form_class = TipoReceitaModelForm
    success_url = reverse_lazy('operacao-list')


class TipoReceitaDeleteView(DeleteView):
    '''EXCLUSÃO DE UM TIPO'''
    model = TipoReceita
    template_name = 'operacao_confirm_delete.html'
    success_url = reverse_lazy('operacao-list')


##### CRUD DE TIPOS DE DESPESAS ######
class TipoDespesaCreateView(CreateView):
    '''CRIAÇÃO DE UM TIPO DE DESPESA'''
    model = TipoDespesa
    template_name = 'operacao_form.html'
    form_class = TipoDespesaModelForm
    success_url = reverse_lazy('operacao-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'AT'  # Define o status como ativo por padrão
        return initial


class TipoDespesaDetailView(DetailView):
    '''DETALHAMENTO DE UM TIPO DE DESPESA'''
    model = TipoDespesa
    template_name = 'receita/receita_detail.html'
    context_object_name = 'tipo'


class TipoDespesaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM TIPO DE DESPESA'''
    model = TipoDespesa
    template_name = 'operacao_form.html'
    form_class = TipoDespesaModelForm
    success_url = reverse_lazy('operacao-list')


class TipoDespesaDeleteView(DeleteView):
    '''EXCLUSÃO DE UM TIPO DE DESPESA'''
    model = TipoDespesa
    template_name = 'operacao_confirm_delete.html'
    success_url = reverse_lazy('operacao-list')


##### CRUD DE TIPOS DE PAGAMENTOS ######
class TipoPagamentoCreateView(CreateView):
    '''CRIAÇÃO DE UM TIPO DE PAGAMENTOS'''
    model = TipoPagamento
    template_name = 'operacao_form.html'
    form_class = TipoPagamentoModelForm
    success_url = reverse_lazy('operacao-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'AT'  # Define o status como ativo por padrão
        return initial


class TipoPagamentoDetailView(DetailView):
    '''DETALHAMENTO DE UM TIPO DE PAGAMENTOS'''
    model = TipoPagamento
    template_name = 'receita/receita_detail.html'
    context_object_name = 'tipo'


class TipoPagamentoUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM TIPO DE PAGAMENTOS'''
    model = TipoPagamento
    template_name = 'operacao_form.html'
    form_class = TipoPagamentoModelForm
    success_url = reverse_lazy('operacao-list')


class TipoPagamentoDeleteView(DeleteView):
    '''EXCLUSÃO DE UM TIPO DE PAGAMENTOS'''
    model = TipoPagamento
    template_name = 'operacao_confirm_delete.html'
    success_url = reverse_lazy('operacao-list')
