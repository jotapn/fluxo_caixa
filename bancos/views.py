from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from movimentacoes.models import Entrada, Saida
from .models import Banco, ContaBancaria
from .forms import BancoModelForm, ContaBancariaModelForm, ContaBancariaUpdateModelForm


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
    
    def form_valid(self, form):
        cb = form.save(commit=False)
        cb.saldo_atual += cb.saldo_inicial
        return super().form_valid(form)
    

class ContaBancariaDetailView(DetailView):
    '''DETALHAMENTO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    template_name = 'conta_bancaria_detail.html'
    context_object_name = 'conta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pegar as movimentações (entradas e saídas) da conta bancária atual
        conta = self.get_object()
        movimentacoes = list(Entrada.objects.filter(conta=conta).order_by('-data')) + list(Saida.objects.filter(conta=conta).order_by('-data'))

        # Agrupar valores por data
        valores_por_data = {}
        for operacao in movimentacoes:
            data_formatada = operacao.data.strftime("%d/%m/%Y")  # Formatação da data
            tipo = 'entrada' if not hasattr(operacao, 'tipo_despesa') else 'saida'
            valor = float(operacao.valor)

            if data_formatada not in valores_por_data:
                valores_por_data[data_formatada] = {'entrada': 0, 'saida': 0}

            valores_por_data[data_formatada][tipo] += valor

        # Ordenar por data
        datas_ordenadas = sorted(valores_por_data.keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"))

        # Prepare os dados para o gráfico
        context['labels'] = datas_ordenadas
        context['entradas'] = [valores_por_data[data]['entrada'] for data in datas_ordenadas]
        context['saidas'] = [valores_por_data[data]['saida'] for data in datas_ordenadas]
        context['movimentacoes'] = movimentacoes

        return context

class ContaBancariaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    form_class = ContaBancariaUpdateModelForm
    template_name = 'conta_bancaria_form.html'
    success_url = reverse_lazy('conta_bancaria_list')

    def form_valid(self, form):
        cb = self.get_object()
        saldo_inicial_antigo = cb.saldo_inicial
        saldo_atual_antigo = cb.saldo_atual
        nova_cb = form.save(commit=False)

        if saldo_inicial_antigo != nova_cb.saldo_inicial:
            form.add_error('saldo_inicial', "Não é permitido alterar o saldo inicial de uma conta já cadastrada.")
            return self.form_invalid(form)
        
        if saldo_atual_antigo != nova_cb.saldo_atual:
            form.add_error('saldo_atual', "Não é permitido alterar o saldo atual.")
            return self.form_invalid(form)

        
        nova_cb.save()
        return super().form_valid(form)
    

class ContaBancariaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    template_name = 'conta_bancaria_confirm_delete.html'
    success_url = reverse_lazy('conta_bancaria_list')