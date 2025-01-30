from django.contrib import admin
from .models import (
    Movimentacao,
    RateioCentroDeCusto,
    Parcela,
    FormaRecebimento
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
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = [
        'descricao', 
        'tipo_movimentacao', 
        'valor', 
        'parcelado', 
        'forma_recebimento', 
        'data_movimentacao', 
        'data_vencimento',
        'pago'
    ]  # Campos exibidos na listagem
    list_filter = ['parcelado', 'forma_recebimento']  # Filtros laterais no admin
    search_fields = ['descricao', 'cadastro__nome', 'centro_de_custo__titulo']  # Campos para busca
    inlines = [RateioCentroDeCustoInline, ParcelaInline]  # Adiciona os inlines para rateios e parcelas
    date_hierarchy = 'data_movimentacao'  # Permite filtrar por hierarquia de datas


    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método de salvar para gerar parcelas automaticamente, se necessário.
        """
        super().save_model(request, obj, form, change)
        if obj.parcelado and not obj.parcelas.exists():
            # Exemplo de geração de 3 parcelas automáticas
            obj.gerar_parcelas(total_parcelas=3, data_inicial=obj.data_vencimento)


# Registro do modelo Rateio de Centros de Custo
@admin.register(RateioCentroDeCusto)
class RateioCentroDeCustoAdmin(admin.ModelAdmin):
    list_display = ['movimentacao', 'centro_de_custo', 'tipo_rateio', 'valor', 'percentual']
    list_filter = ['tipo_rateio', 'centro_de_custo']
    search_fields = ['movimentacao__descricao', 'centro_de_custo__titulo']


