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
    
class ContaBancariaListView(ListView):
    '''LISTAGEM DE CONTAS BANCÁRIAS'''
    model = ContaBancaria
    template_name = 'conta_bancaria_list.html'
    context_object_name = 'contas'


class ContaBancariaUpdateView(UpdateView):
    model = ContaBancaria
    form_class = ContaBancariaUpdateModelForm
    template_name = 'conta_bancaria_form.html'  # Substitua pelo caminho do seu template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operacao'] = 'update'
        print(context)
        return context

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

        context['movimentacoes'] = movimentacoes

        # Prepare os dados para o gráfico (agregados por mês)
        valores_por_mes = {}
        for operacao in movimentacoes:
            mes_ano = operacao.data.strftime("%m/%Y")  # Formatação do mês e ano
            tipo = 'entrada' if not hasattr(operacao, 'tipo_despesa') else 'saida'
            valor = float(operacao.valor)

            if mes_ano not in valores_por_mes:
                valores_por_mes[mes_ano] = {'entrada': 0, 'saida': 0}

            valores_por_mes[mes_ano][tipo] += valor

        # Ordenar por mês
        meses_ordenados = sorted(valores_por_mes.keys(), key=lambda x: datetime.strptime(x, "%m/%Y"))

        entradas = [valores_por_mes[mes]['entrada'] for mes in meses_ordenados]
        saidas = [valores_por_mes[mes]['saida'] for mes in meses_ordenados]
        lucro_prejuizo = [valores_por_mes[mes]['entrada'] - valores_por_mes[mes]['saida'] for mes in meses_ordenados]

        # Prepare os dados para o gráfico
        context['labels'] = meses_ordenados
        context['entradas'] = entradas
        context['saidas'] = saidas
        context['lp'] = lucro_prejuizo

        return context

class ContaBancariaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA CONTA BANCÁRIA'''
    model = ContaBancaria
    template_name = 'conta_bancaria_confirm_delete.html'
    success_url = reverse_lazy('conta_bancaria_list')