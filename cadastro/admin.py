from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Pessoa, Endereco, TipoEndereco

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cep','logradouro', )
    search_fields = ('cep', )

# Formset personalizado para garantir a validação do endereço principal
class EnderecoInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Validar que há pelo menos um endereço principal
        has_principal = False
        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False):  # Ignorar exclusões
                if form.cleaned_data.get("tipo") == TipoEndereco.PRINCIPAL:
                    if has_principal:
                        raise ValidationError("Apenas um endereço pode ser marcado como principal.")
                    has_principal = True

        if not has_principal:
            raise ValidationError("É obrigatório ter pelo menos um endereço principal.")

# Inline para gerenciar os endereços
class EnderecoInline(admin.StackedInline):
    model = Endereco
    formset = EnderecoInlineFormSet
    fields = ['tipo', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'estado', 'pais']
    extra = 0  # Valor padrão para evitar formulários extras

    def get_extra(self, request, obj=None, **kwargs):
        """
        Retorna 1 formulário extra apenas se não houver nenhum endereço cadastrado.
        """
        if obj and obj.enderecos.exists():
            return 0  # Nenhum formulário extra se já houver endereços cadastrados
        return 1  # Um formulário extra se nenhum endereço existir

# Configuração do admin para Cadastro
@admin.register(Pessoa)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'endereco_principal']
    inlines = [EnderecoInline]

    def endereco_principal(self, obj):
        # Exibe o endereço principal na listagem do admin
        principal = obj.enderecos.filter(tipo=TipoEndereco.PRINCIPAL).first()
        if principal:
            return f"{principal.logradouro}, {principal.numero} - {principal.municipio}/{principal.estado}"
        return "Nenhum principal"
    endereco_principal.short_description = "Endereço Principal"
