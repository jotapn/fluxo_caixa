from django.contrib import admin
from .models import Entrada, Saida, Transacao, Categoria

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    def delete_all_entries(modeladmin, request, queryset):
        queryset.delete()

    list_display = ('cliente', 'descricao', 'valor', 'data', 'tipo_pagamento', 'situacao')
    search_fields = ('descricao', "cliente" )  
    list_filter = ('data', 'tipo_pagamento', 'situacao')
    actions = [delete_all_entries]

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    def delete_all_saidas(modeladmin, request, queryset):
        queryset.delete()
    list_display = ("tipo_despesa", 'descricao', 'valor', 'data', 'tipo_pagamento', 'situacao')
    search_fields = ('descricao', "tipo_despesa")  
    list_filter = ('data', 'tipo_pagamento', 'situacao')
    actions = [delete_all_saidas]

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ("tipo_transacao", 'titulo', 'valor', 'data', 'metodo_pagamento', 'situacao')
    search_fields = ("titulo", "tipo_transacao")
    list_filter = ("situacao", "tipo_transacao")


@admin.register(Categoria)
class TipoPagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_transacao' )
    search_fields = ('nome',)
    list_filter = ('tipo_transacao',)