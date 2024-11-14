from django import forms
from django.utils.timezone import now, datetime
from .models import Entrada, Saida
from bancos.models import ContaBancaria
from operacoes.models import TipoDespesa, TipoPagamento, TipoReceita

class EntradaModelForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        initial=datetime.today,
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Entrada
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'placeholder':'0,00'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar para exibir apenas os bancos ativos
        self.fields['conta'].queryset = ContaBancaria.objects.filter(status='AT')
        self.fields['tipo_pagamento'].queryset = TipoPagamento.objects.filter(status='AT')
        self.fields['tipo_receita'].queryset = TipoReceita.objects.filter(status='AT')

class SaidaModelForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        initial=datetime.today,
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Saida
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'placeholder':'0,00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conta'].queryset = ContaBancaria.objects.filter(status='AT')
        self.fields['tipo_pagamento'].queryset = TipoPagamento.objects.filter(status='AT')
        self.fields['tipo_despesa'].queryset = TipoDespesa.objects.filter(status='AT')
