from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from operacoes.models import NaturezaFinanceira, SinalNatureza
from .models import (
    Movimentacao,
    RateioCentroDeCusto,
    Parcela,
    FormaRecebimento,
    TipoMovimentacao,
    HistoricoTransacao,
    CondicaoPagamento
)

# Inline para Rateio de Centros de Custo
class RateioCentroDeCustoInline(admin.TabularInline):
    model = RateioCentroDeCusto
    extra = 1  # Número de formulários extras para novos rateios
    fields = ['centro_de_custo', 'tipo_rateio', 'valor', 'percentual']  # Campos exibidos no admin

    def get_extra(self, request, obj=None, **kwargs):
        """Não mostrar formulário extra se já houver rateios."""
        return 0 if obj and obj.rateios.exists() else 1


# Inline para Parcelas
class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 1  # Número de formulários extras para novas parcelas
    fields = ['numero', 'valor', 'data_vencimento', 'pago']  # Campos exibidos no admin
    readonly_fields = ['numero', 'valor', 'data_vencimento']  # Campos gerados automaticamente são somente leitura

    def get_extra(self, request, obj=None, **kwargs):
        """Não mostrar formulário extra se já houver parcelas."""
        return 0 if obj and obj.parcelas.exists() else 1


# Registro do modelo Forma de Recebimento
@admin.register(FormaRecebimento)
class FormaRecebimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']  # Exibe nome e status no admin
    list_filter = ['ativo']  # Filtro por status ativo/inativo
    search_fields = ['nome']  # Campo de busca pelo nome


# Registro do modelo Movimentação
@admin.register(Movimentacao)
class MovimentacaoAdmin(SimpleHistoryAdmin, admin.ModelAdmin):  # 🔥 Corrigido!
    list_display = [
        'descricao', 
        'tipo_movimentacao', 
        'valor', 
        'data_vencimento',
    ]
    list_filter = ['forma_recebimento']
    search_fields = ['descricao', 'cadastro__nome', 'centro_de_custo__titulo']
    inlines = [RateioCentroDeCustoInline, ParcelaInline]
    date_hierarchy = 'data_movimentacao'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "natureza_financeira":
            tipo_movimentacao = request.GET.get("tipo_movimentacao", None)
            if tipo_movimentacao == TipoMovimentacao.RECEITA:
                kwargs["queryset"] = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.CREDITO)
            elif tipo_movimentacao == TipoMovimentacao.DESPESA:
                kwargs["queryset"] = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.DEBITO)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Registro do modelo Rateio de Centros de Custo
@admin.register(RateioCentroDeCusto)
class RateioCentroDeCustoAdmin(admin.ModelAdmin):
    list_display = ['movimentacao', 'centro_de_custo', 'tipo_rateio', 'valor', 'percentual']
    list_filter = ['tipo_rateio', 'centro_de_custo']
    search_fields = ['movimentacao__descricao', 'centro_de_custo__titulo']

@admin.register(HistoricoTransacao)
class HistoricoTransacaoAdmin(admin.ModelAdmin):
    list_display = ("transacao", 'data_movimentacao', 'tipo_movimentacao', 'valor', 'saldo_anterior', 'saldo_posterior', 'conta_bancaria')
    list_filter = ("transacao", 'data_movimentacao', 'tipo_movimentacao', 'conta_bancaria')
    search_fields = ("transacao", 'data_movimentacao', 'tipo_movimentacao', 'conta_bancaria')

@admin.register(CondicaoPagamento)
class CondicaoPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome',]
    list_filter = ['nome', ]