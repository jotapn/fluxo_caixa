from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Pessoa, Endereco
from . forms import PessoaForm

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cep','logradouro', )
    search_fields = ('cep', )

# Formset personalizado para garantir a validação do endereço principal
class EnderecoInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_principal = False
        for form in self.forms:
            if form.cleaned_data.get("DELETE", False):
                continue  # Ignora os endereços marcados para exclusão
            
            if form.cleaned_data.get("principal", False):
                if has_principal:
                    raise ValidationError("Apenas um endereço pode ser marcado como principal.")
                has_principal = True

        if not has_principal:
            raise ValidationError("É obrigatório ter pelo menos um endereço principal.")

# Inline para gerenciar os endereços
class EnderecoInline(admin.StackedInline):
    model = Endereco
    formset = EnderecoInlineFormSet
    fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'estado', 'pais', 'principal']
    extra = 1  # Valor padrão para evitar formulários extras

    def get_extra(self, request, obj=None, **kwargs):
        """
        Retorna 1 formulário extra apenas se não houver nenhum endereço cadastrado.
        """
        if obj is None or not obj.enderecos.exists():
            return 1  # Se obj não existir ou não tiver endereços, exibe um formulário extra
        return 0  # Um formulário extra se nenhum endereço existir

# Configuração do admin para Cadastro
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_pessoa', 'email', 'telefone', 'endereco_principal']
    form = PessoaForm
    inlines = [EnderecoInline]
    list_filter = ['tipo_pessoa']
    search_fields = ['nome', 'email', 'telefone', 'cnpj_cpf']
    list_editable = ['telefone']

    def atributos_list(self, obj):
        """Exibe os atributos como texto no Django Admin."""
        return ", ".join(obj.get_atributos_display()) if obj.atributos else "Nenhum"
    
    atributos_list.short_description = "Atributos"
    
    def endereco_principal(self, obj):
        endereco = obj.enderecos.filter(principal=True).first()
        if endereco:
            return f"{endereco.logradouro}, {endereco.numero} - {endereco.municipio}/{endereco.estado}"
        return "Nenhum principal"
    endereco_principal.short_description = "Endereço Principal"
