from django.contrib import admin
from .models import TipoReceita, TipoDespesa, TipoPagamento

@admin.register(TipoReceita)
class TipoReceitaAdmin(admin.ModelAdmin):
    list_display = ('nome','status')
    search_fields = ('nome',)
    list_filter = ('status',)


@admin.register(TipoDespesa)
class TipoDespesaAdmin(admin.ModelAdmin):
    list_display = ('nome','status')
    search_fields = ('nome',)
    list_filter = ('status',)

@admin.register(TipoPagamento)
class TipoPagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome','status')
    search_fields = ('nome',)
    list_filter = ('status',)
