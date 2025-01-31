from django import forms
from .models import Movimentacao, TipoMovimentacao
from operacoes.models import NaturezaFinanceira, SinalNatureza

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pegamos o valor inicial de 'tipo_movimentacao'
        tipo_movimentacao = self.initial.get('tipo_movimentacao', None)
        
        # Aplicamos o filtro correto na natureza financeira
        if tipo_movimentacao == TipoMovimentacao.RECEITA:
            self.fields['natureza_financeira'].queryset = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.CREDITO)
        elif tipo_movimentacao == TipoMovimentacao.DESPESA:
            self.fields['natureza_financeira'].queryset = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.DEBITO)
