from django.contrib import admin
from .models import CentroDeCusto, NaturezaFinanceira

@admin.register(CentroDeCusto)
class CentroDeCustoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'status')
    list_filter = ('status',)
    search_fields = ('codigo', 'titulo')

@admin.register(NaturezaFinanceira)
class NaturezaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'status')
    list_filter = ('status','tipo', 'sinal')
    search_fields = ('codigo', 'titulo')