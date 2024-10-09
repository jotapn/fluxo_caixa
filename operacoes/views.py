from django.urls import reverse_lazy
from django.shortcuts import redirect
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

        # Unificando as operações com os campos comuns
        operacoes = []
        for receita in tipo_receita:
            operacoes.append({
                'nome': receita.nome,
                'tipo': 'Receita',
                'status': receita.status_formatado,
                'objeto': receita
            })
        for despesa in tipo_despesa:
            operacoes.append({
                'nome': despesa.nome,
                'tipo': 'Despesa',
                'status': despesa.status_formatado,
                'objeto': despesa
            })
        for pagamento in tipo_pagamento:
            operacoes.append({
                'nome': pagamento.nome,
                'tipo': 'Pagamento',
                'status': pagamento.status_formatado,
                'objeto': pagamento
            })

        context['operacoes'] = operacoes
        return context


class CriarOperacaoView(TemplateView):
    template_name = 'operacao_criar.html'

    def post(self, request, *args, **kwargs):
        tipo_operacao = request.POST.get('tipo_operacao')

        if tipo_operacao == 'receita':
            return redirect('tipo_receita_create')
        elif tipo_operacao == 'despesa':
            return redirect('tipo_despesa_create')
        elif tipo_operacao == 'pagamento':
            return redirect('tipo_pagamento_create')
        else:
            return self.render_to_response(self.get_context_data(error='Selecione um tipo de operação.'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
