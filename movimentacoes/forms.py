from django import forms
from .models import Entrada, Saida
from datetime import date, datetime
from django.utils.timezone import now


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
        }

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
        }

