from django import forms
from .models import Entrada, Saida


class EntradaModelForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = "__all__"


class SaidaModelForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = "__all__"
