from django import forms
from .models import TipoReceita, TipoDespesa, TipoPagamento

class TipoReceitaModelForm(forms.ModelForm):
    class Meta:
        model = TipoReceita
        fields = '__all__'

class TipoDespesaModelForm(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        fields = '__all__'

class TipoPagamentoModelForm(forms.ModelForm):
    class Meta:
        model = TipoPagamento
        fields = '__all__'