from django.contrib import admin
from clientes.models import Cliente

class ClientesAdmin(admin.ModelAdmin):
    list_display=("nome_fantasia", "razao_social", "cnpj_cpf", "cep", 'endereco')
    search_fields = ("nome_fantasia", "cnpj_cpf")

admin.site.register(Cliente, ClientesAdmin)