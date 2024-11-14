import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from bancos.models import ContaBancaria
from .models import Entrada, Saida
from .forms import EntradaModelForm, SaidaModelForm
from django.shortcuts import render, redirect
from .tasks import importar_entradas_task, importar_saidas_task
from django.core.files.storage import default_storage

##### CRUD DE ENTRADAS ######
class EntradaListView(ListView):
    '''LISTAGEM DE ENTRADAS'''
    model = Entrada
    template_name = 'entrada/entrada_list.html'
    context_object_name = 'entradas'

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
        entrada = form.save(commit=False)

        entradas_existentes = Entrada.objects.filter(
            cliente=entrada.cliente,
            descricao=entrada.descricao,
            valor=entrada.valor,
            data=entrada.data,
            conta=entrada.conta,
            tipo_pagamento=entrada.tipo_pagamento,
            situacao=entrada.situacao
        )

        if entradas_existentes.exists():
            if self.request.POST.get('confirm_duplicate') != 'true':
                # Passa a flag ao template se existir uma duplicidade
                context = self.get_context_data(form=form)
                context['duplicate_warning'] = True
                return self.render_to_response(context)
            
        messages.add_message(self.request, constants.SUCCESS, "Receita criada com sucesso")
        entrada.save() 
        return super().form_valid(form)


class EntradaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_form.html'
    form_class = EntradaModelForm
    success_url = reverse_lazy('entrada-list')
    
    def form_valid(self, form):
        entrada = form.save(commit=False)

        # Verifica se a saída já existe
        entrada_existente = Entrada.objects.filter(
            cliente=entrada.cliente,
            descricao=entrada.descricao,
            valor=entrada.valor,
            data=entrada.data,
            conta=entrada.conta,
            tipo_pagamento=entrada.tipo_pagamento,
            situacao=entrada.situacao
        )

        context = self.get_context_data(form=form)
        context['duplicate_warning'] = False

        # Verifica as condições de duplicidade e saldo negativo
        if entrada_existente.exists():
            context['duplicate_warning'] = True

        # Lógica para lidar com confirmações
        if context['duplicate_warning'] and self.request.POST.get('confirm_duplicate') != 'true':
            return self.render_to_response(context)

        messages.add_message(self.request, constants.SUCCESS, "Receita editada com sucesso")
        return super().form_valid(form)
    

class EntradaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA ENTRADA'''
    model = Entrada
    template_name = 'entrada/entrada_confirm_delete.html'
    success_url = reverse_lazy('entrada-list')
    
    def post(self, request, pk):
        entrada = get_object_or_404(Entrada, pk=pk)
        entrada.delete()
        # Mensagem de sucesso
        messages.add_message(request,constants.SUCCESS, 'Receita excluída com sucesso e saldo ajustado.')
        # Redireciona para a página de listagem
        return redirect(self.success_url)

##### CRUD DE SAÍDAS ######
class SaidaListView(ListView):
    '''LISTAGEM DE SAÍDAS'''
    model = Saida
    template_name = 'saida/saida_list.html'
    context_object_name = 'saidas'
    ordering = ['data']

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

        # Verifica se a saída já existe
        saida_existente = Saida.objects.filter(
            descricao=saida.descricao,
            valor=saida.valor,
            data=saida.data,
            conta=saida.conta,
            tipo_pagamento=saida.tipo_pagamento,
            situacao=saida.situacao
        )

        novo_saldo = saida.conta.saldo_atual - saida.valor if saida.situacao == "PG" else saida.conta.saldo_atual
        context = self.get_context_data(form=form)
        context['saldo_negativo'] = False
        context['duplicate_warning'] = False

        # Verifica as condições de duplicidade e saldo negativo
        if saida_existente.exists():
            context['duplicate_warning'] = True
        if saida.situacao == "PG" and novo_saldo < 0:
            context['saldo_negativo'] = True

        # Lógica para lidar com confirmações
        if context['duplicate_warning'] and self.request.POST.get('confirm_duplicate') != 'true':
            return self.render_to_response(context)

        if context['saldo_negativo'] and self.request.POST.get('confirm_saldo_negativo') != 'true':
            return self.render_to_response(context)

        messages.add_message(self.request, constants.SUCCESS, "Despesa criada com sucesso")
        return super().form_valid(form)
    



class SaidaUpdateView(UpdateView):
    '''ATUALIZAÇÃO DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_form.html'
    form_class = SaidaModelForm
    success_url = reverse_lazy('saida-list')

    def form_valid(self, form):
        saida = form.save(commit=False)
        # Verifica se a saída já existe
        saida_existente = Saida.objects.filter(
            descricao=saida.descricao,
            valor=saida.valor,
            data=saida.data,
            conta=saida.conta,
            tipo_pagamento=saida.tipo_pagamento,
            situacao=saida.situacao
        ).exclude(pk=saida.pk)

        context = self.get_context_data(form=form)
        context['saldo_negativo'] = False
        context['duplicate_warning'] = False

        # Verifica as condições de duplicidade e saldo negativo
        if saida_existente.exists():
            context['duplicate_warning'] = True

        if saida.situacao == "PG" and saida.conta.saldo_atual - saida.valor < 0:
            context['saldo_negativo'] = True

        # Lógica para lidar com confirmações
        if context['duplicate_warning'] and self.request.POST.get('confirm_duplicate') != 'true':
            return self.render_to_response(context)

        if context['saldo_negativo'] and self.request.POST.get('confirm_saldo_negativo') != 'true':
            return self.render_to_response(context)

        messages.add_message(self.request, constants.SUCCESS, "Despesa editada com sucesso")
        return super().form_valid(form)


class SaidaDeleteView(DeleteView):
    '''EXCLUSÃO DE UMA SAÍDA'''
    model = Saida
    template_name = 'saida/saida_confirm_delete.html'
    success_url = reverse_lazy('saida-list')
    
    def post(self, request, pk):
        saida = get_object_or_404(Saida, pk=pk)
        saida.delete()
        # Mensagem de sucesso
        messages.add_message(request,constants.SUCCESS, 'Despesa excluída com sucesso e saldo ajustado.')

        # Redireciona para a página de listagem
        return redirect(self.success_url)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.date.today()
        mes = int(self.request.GET.get('mes', today.month))
        ano = int(self.request.GET.get('ano', today.year))

        entradas = Entrada.objects.filter(data__month=mes, data__year=ano).order_by('data')
        saidas = Saida.objects.filter(data__month=mes, data__year=ano).order_by('data')
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


def importar_entradas_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = f'/tmp/{file.name}'
        
        # Salva o arquivo temporariamente
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Chama a task assíncrona
        importar_entradas_task.delay(file_path)
        
        # Redireciona para a página de sucesso
        messages.success(request, 'A importação de entradas foi iniciada e está sendo processada.')
        return redirect('sucesso')

    return render(request, 'importacoes/importar_entradas.html')

def importar_saidas_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = f'/tmp/{file.name}'
        
        # Salva o arquivo temporariamente
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Chama a task assíncrona
        importar_saidas_task.delay(file_path)
        
        # Redireciona para a página de sucesso
        messages.success(request, 'A importação de saídas foi iniciada e está sendo processada.')
        return redirect('sucesso')

    return render(request, 'importacoes/importar_saidas.html')


class SucessoView(TemplateView):
    template_name = 'sucesso.html'
