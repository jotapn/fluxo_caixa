from django import forms
from .models import Banco, ContaBancaria


class BancoModelForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ("nome", "status")

class ContaBancariaModelForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'