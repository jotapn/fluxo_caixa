from django import forms
from .models import Banco, Tipo, Entrada, Saida


class BancoModelForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ("nome", "saldo_inicial", "status")


class TipoModelForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = '__all__'


class EntradaModelForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = "__all__"


class SaidaModelForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = "__all__"
