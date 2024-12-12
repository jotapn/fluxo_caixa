from django.contrib import admin
from .models import OperacaoFinanceira, CentroDeCusto, NaturezaFinanceira

@admin.register(NaturezaFinanceira)
class NaturezaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('codigo', "nome", "ativo")
    search_fields = ('nome',)

@admin.register(CentroDeCusto)
class CentroDeCustoAdmin(admin.ModelAdmin):
    list_display = ('codigo', "nome", "ativo")
    search_fields = ('nome',)
# Register your models here.

@admin.register(OperacaoFinanceira)
class OperacaoFinanceiraAdmin(admin.ModelAdmin):
    list_display=('pessoa', "data_vencimento", "valor", "pago")
    search_fields = ("pessoa", )
    list_filter = ("pago", "conta")