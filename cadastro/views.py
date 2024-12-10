from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Cadastro
from .forms import CadastroForm

def criar_cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cadastros')  # Redirecionar após salvar
    else:
        form = CadastroForm()
    return render(request, 'criar_cadastro.html', {'form': form})


class CadastroListView(ListView):
    model = Cadastro
    template_name = "cadastro.html"
    context_object_name = 'cadastros'

    def get_queryset(self):
        cadastro = super().get_queryset().order_by('nome')
        search = self.request.GET.get('search')
        if search:
            cadastro = cadastro.filter(model__icontains=search)
        return cadastro