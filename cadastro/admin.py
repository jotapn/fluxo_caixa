from django.contrib import admin
from .models import Cadastro, Atributo
from .forms import CadastroForm

@admin.register(Atributo)
class AtributoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)

@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    form = CadastroForm
    list_display = ('nome_fantasia', 'cnpj_cpf', 'mostrar_atributos')
    list_filter = ('atributos',)  # Adiciona filtro por atributos
    search_fields = ('nome_fantasia', 'cnpj_cpf')

    def mostrar_atributos(self, obj):
        return ", ".join([atributo.tipo for atributo in obj.atributos.all()])

    mostrar_atributos.short_description = "Atributos"  # Nome da coluna no Django Admin