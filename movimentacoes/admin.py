from django.contrib import admin
from .models import Banco, Tipo, Entrada, Saida

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'saldo_atual', 'status')
    search_fields = ('nome',)
    list_filter = ('status',)

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'status')
    search_fields = ('nome',)
    list_filter = ('tipo', 'status')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    def delete_all_entries(modeladmin, request, queryset):
        queryset.delete()

    list_display = ('cliente', 'descricao', 'valor', 'data', 'banco', 'tipo_pagamento', 'situacao')
    search_fields = ('descricao', "cliente" )  
    list_filter = ('data', 'banco', 'tipo_pagamento', 'situacao')
    actions = [delete_all_entries]

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    def delete_all_saidas(modeladmin, request, queryset):
        queryset.delete()
    list_display = ("tipo_despesa", 'descricao', 'valor', 'data', 'banco', 'tipo_pagamento', 'situacao')
    search_fields = ('descricao', "tipo_despesa")  
    list_filter = ('data', 'banco', 'tipo_pagamento', 'situacao')
    actions = [delete_all_saidas]
