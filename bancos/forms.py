from django import forms
from .models import Banco, ContaBancaria


class BancoModelForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ("nome", "status")

class ContaBancariaModelForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        fields = '__all__'
        widgets = {
            'saldo_atual': forms.NumberInput(attrs={"readonly":True}),
            'saldo_inicial': forms.NumberInput(attrs={'placeholder':'0,00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar para exibir apenas os bancos ativos
        self.fields['banco'].queryset = Banco.objects.filter(status='AT')

class ContaBancariaUpdateModelForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        fields = '__all__'
        widgets = {
            'saldo_atual': forms.NumberInput(attrs={"readonly":True}),
            'saldo_inicial': forms.NumberInput(attrs={"readonly":True}),
        }

class FiltroMovimentacaoForm(forms.Form):
    class Meta:
        fields = ['situacao', 'data_inicio', 'data_fim'] 
        situacao_choices = [
        ('', 'Todas'),
        ('PG', 'Pago'),
        ('AP', 'A pagar'),
        ]
        situacao = forms.ChoiceField(choices=situacao_choices, required=False)
        data_inicio = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
        data_fim = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

