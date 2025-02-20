from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Pessoa
from .forms import PessoaForm

def criar_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cadastros')  # Redirecionar após salvar
    else:
        form = PessoaForm()
    return render(request, 'criar_cadastro.html', {'form': form})


class PessoaListView(ListView):
    model = Pessoa
    template_name = "cadastro.html"
    context_object_name = 'cadastros'

    def get_queryset(self):
        cadastro = super().get_queryset().order_by('nome')
        search = self.request.GET.get('search')
        if search:
            cadastro = cadastro.filter(model__icontains=search)
        return cadastro