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

class ContaBancariaUpdateModelForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        fields = '__all__'
        widgets = {
            'saldo_atual': forms.NumberInput(attrs={"readonly":True}),
            'saldo_inicial': forms.NumberInput(attrs={"readonly":True}),
        }