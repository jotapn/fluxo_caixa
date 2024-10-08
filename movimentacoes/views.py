from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Banco, Tipo, Entrada, Saida
from .forms import BancoModelForm, TipoModelForm, EntradaModelForm, SaidaModelForm
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.contrib import messages


##### CRUD DE BANCOS ######
class BancoCreateView(CreateView):
    '''CRIAÇÃO DE UM NOVO BANCO'''
    model = Banco
    form_class = BancoModelForm
    template_name = 'banco/banco_form.html'
    success_url = reverse_lazy('banco-list')


class BancoListView(ListView):
    '''LISTAGEM DOS BANCOS'''
    model = Banco
    template_name = 'banco/banco_list.html'
    context_object_name = 'bancos'


class BancoDetailView(DetailView):
    '''DETALHAMENTO DE UM BANCO'''
    model = Banco
    template_name = 'banco/banco_detail.html'
    context_object_name = 'banco'


class BancoUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM BANCO'''
    model = Banco
    template_name = 'banco/banco_form.html'
    form_class = BancoModelForm
    success_url = reverse_lazy('banco-list')
    
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

import logging

logger = logging.getLogger(__name__)

class BancoDeleteView(DeleteView):
    '''EXCLUSÃO DE UM BANCO'''
    model = Banco
    template_name = 'banco/banco_confirm_delete.html'
    success_url = reverse_lazy('banco-list')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Não é possível excluir este banco porque ele está relacionado a outras operações.")
            return self.get(request, *args, **kwargs)



##### CRUD DE TIPOS ######
class TipoListView(ListView):
    '''LISTAGEM DE TIPOS'''
    model = Tipo
    template_name = 'tipo/tipo_list.html'
    context_object_name = 'tipos'


class TipoDetailView(DetailView):
    '''DETALHAMENTO DE UM TIPO'''
    model = Tipo
    template_name = 'tipo/tipo_detail.html'
    context_object_name = 'tipo'


class TipoCreateView(CreateView):
    '''CRIAÇÃO DE UM TIPO'''
    model = Tipo
    template_name = 'tipo/tipo_form.html'
    form_class = TipoModelForm
    success_url = reverse_lazy('tipo-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'AT'  # Define o status como ativo por padrão
        return initial


class TipoUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UM TIPO'''
    model = Tipo
    template_name = 'tipo/tipo_form.html'
    form_class = TipoModelForm
    success_url = reverse_lazy('tipo-list')


class TipoDeleteView(DeleteView):
    '''EXCLUSÃO DE UM TIPO'''
    model = Tipo
    template_name = 'tipo/tipo_confirm_delete.html'
    success_url = reverse_lazy('tipo-list')


##### CRUD DE ENTRADAS ######
class EntradaListView(ListView):
    '''LISTAGEM DE ENTRADAS'''
    model = Entrada
    template_name = 'entrada/entrada_list.html'
    context_object_name = 'entradas'

# Detalhes de uma Entrada
class EntradaDetailView(DetailView):
    '''DETALHAMENTO DE ENTRADAS'''
    model = Entrada
    template_name = 'entrada/entrada_detail.html'
    context_object_name = 'entrada'

class EntradaCreateView(CreateView):
    '''CRIAÇÃO DE ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_form.html'
    form_class = EntradaModelForm
    success_url = reverse_lazy('entrada-list')


class EntradaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_form.html'
    form_class = EntradaModelForm
    success_url = reverse_lazy('entrada-list')


class EntradaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_confirm_delete.html'
    success_url = reverse_lazy('entrada-list')


##### CRUD DE SAÍDAS ######
class SaidaListView(ListView):
    '''LISTAGEM DE SAÍDAS'''
    model = Saida
    template_name = 'saida/saida_list.html'
    context_object_name = 'saidas'


class SaidaDetailView(DetailView):
    '''DETALHES DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_detail.html'
    context_object_name = 'saida'

class SaidaCreateView(CreateView):
    '''CRIAÇÃO DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_form.html'
    form_class = SaidaModelForm
    success_url = reverse_lazy('saida-list')


class SaidaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_form.html'
    form_class = SaidaModelForm
    success_url = reverse_lazy('saida-list')


class SaidaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_confirm_delete.html'
    success_url = reverse_lazy('saida-list')


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pega o mês do GET, se não houver, usa o mês atual
        mes = self.request.GET.get('mes', timezone.now().month)
        ano = timezone.now().year  # você pode querer adicionar uma opção para o ano

        entradas = Entrada.objects.filter(data__month=mes, data__year=ano)
        saidas = Saida.objects.filter(data__month=mes, data__year=ano)
        bancos = Banco.objects.all()

        context['entradas'] = entradas
        context['saidas'] = saidas
        context['mes_atual'] = mes  # Adiciona o mês atual ao contexto
        context['bancos'] = bancos

        # Define a lista de meses
        context['meses'] = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        return context
