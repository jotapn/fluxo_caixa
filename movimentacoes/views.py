from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from bancos.models import ContaBancaria
from .models import Entrada, Saida
from .forms import EntradaModelForm, SaidaModelForm


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


    def form_valid(self, form):
        # Salvar a entrada primeiro
        entrada = form.save(commit=False)
        entradas_existentes = Entrada.objects.filter(
            descricao=entrada.descricao,
            valor=entrada.valor,
            data=entrada.data,
            cliente=entrada.cliente
        )

        if entradas_existentes.exists():
            if self.request.POST.get('confirm_duplicate') != 'true':
                # Passa a flag ao template se existir uma duplicidade
                context = self.get_context_data(form=form)
                context['duplicate_warning'] = True
                return self.render_to_response(context)


        # Atualizar o saldo da conta bancária
        if entrada.situacao == "PG":
            entrada.conta.saldo_atual += entrada.valor
        
        entrada.save()  # Salvar a entrada
        entrada.conta.save()  # Atualizar o saldo da conta bancária
        return super().form_valid(form)


class EntradaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_form.html'
    form_class = EntradaModelForm
    success_url = reverse_lazy('entrada-list')

    def form_valid(self, form):
        # Obter a entrada antiga para comparar os valores anteriores
        entrada_antiga = Entrada.objects.get(pk=self.object.pk)
        entrada_nova = form.save(commit=False)

        conta_bancaria = entrada_nova.conta
        
        # Se a entrada antiga já estava "paga", subtrair o valor antigo do saldo
        if entrada_antiga.situacao == "PG":
            conta_bancaria.saldo_atual -= entrada_antiga.valor

        # Se a nova entrada também está "paga", adicionar o novo valor ao saldo
        if entrada_nova.situacao == "PG":
            conta_bancaria.saldo_atual += entrada_nova.valor

        # Salvar a entrada e a conta bancária
        entrada_nova.save()
        conta_bancaria.save()

        return super().form_valid(form)


class EntradaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_confirm_delete.html'
    success_url = reverse_lazy('entrada-list')
    
    def post(self, request, pk):
        entrada = get_object_or_404(Entrada, pk=pk)

        conta_bancaria = entrada.conta

        # Subtrai o valor da entrada do saldo atual da conta bancária
        conta_bancaria.saldo_atual -= entrada.valor
        conta_bancaria.save()

        # Exclui a entrada
        entrada.delete()

        # Mensagem de sucesso
        messages.add_message(request,constants.SUCCESS, 'Entrada excluída com sucesso e saldo ajustado.')

        # Redireciona para a página de listagem
        return redirect('entrada-list')

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

    def form_valid(self, form):
        saida = form.save(commit=False)

        if saida.situacao == "PG":
            saida.conta.saldo_atual -= saida.valor
        
        saida.save()
        saida.conta.save()
        return super().form_valid(form)
    



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
        contas = ContaBancaria.objects.all()

        context['entradas'] = entradas
        context['saidas'] = saidas
        context['mes_atual'] = mes  # Adiciona o mês atual ao contexto
        context['bancos'] = contas

        # Define a lista de meses
        context['meses'] = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        return context
