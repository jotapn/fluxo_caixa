from django import forms
from django.contrib.auth.models import User
from .models import Movimentacao, TipoMovimentacao, CartaoCredito, PermissaoFinanceira
from operacoes.models import NaturezaFinanceira, SinalNatureza


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'tipo_movimentacao', 'descricao', 'valor', 'condicao_pagamento',
            'natureza_financeira', 'centro_de_custo', 'data_movimentacao',
            'forma_recebimento', 'data_vencimento', 'pessoa', 'conta_bancaria',
            'cartao_credito'
        ]
        widgets = {
            'data_movimentacao': forms.DateInput(attrs={'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pegamos o valor inicial de 'tipo_movimentacao'
        tipo_movimentacao = self.initial.get('tipo_movimentacao', None)
        
        # Aplicamos o filtro correto na natureza financeira
        if tipo_movimentacao == TipoMovimentacao.RECEITA:
            self.fields['natureza_financeira'].queryset = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.CREDITO)
            self.fields['cartao_credito'].widget = forms.HiddenInput()
            self.fields['centro_de_custo'].widget = forms.HiddenInput()
        elif tipo_movimentacao == TipoMovimentacao.DESPESA:
            self.fields['natureza_financeira'].queryset = NaturezaFinanceira.objects.filter(sinal=SinalNatureza.DEBITO)

        # Se o usuário não tem permissão para ver todas as movimentações,
        # filtra apenas os cartões ativos
        if user and not hasattr(user, 'permissaofinanceira') or not user.permissaofinanceira.pode_gerenciar_cartoes:
            self.fields['cartao_credito'].queryset = CartaoCredito.objects.filter(ativo=True)

    def clean(self):
        cleaned_data = super().clean()
        tipo_movimentacao = cleaned_data.get('tipo_movimentacao')
        centro_de_custo = cleaned_data.get('centro_de_custo')
        cartao_credito = cleaned_data.get('cartao_credito')

        if tipo_movimentacao == TipoMovimentacao.DESPESA and not centro_de_custo:
            raise forms.ValidationError('Centro de custo é obrigatório para despesas')

        if cartao_credito and tipo_movimentacao == TipoMovimentacao.RECEITA:
            raise forms.ValidationError('Cartão de crédito só pode ser usado em despesas')

        if cartao_credito:
            valor = cleaned_data.get('valor', 0)
            if valor > cartao_credito.limite_disponivel:
                raise forms.ValidationError('Valor excede o limite disponível do cartão')

        return cleaned_data


class CartaoCreditoForm(forms.ModelForm):
    class Meta:
        model = CartaoCredito
        fields = ['nome', 'banco', 'dia_corte', 'dia_vencimento', 'limite', 'limite_disponivel', 'ativo']
        widgets = {
            'limite': forms.NumberInput(attrs={'step': '0.01'}),
            'limite_disponivel': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dia_corte = cleaned_data.get('dia_corte')
        dia_vencimento = cleaned_data.get('dia_vencimento')
        limite = cleaned_data.get('limite')
        limite_disponivel = cleaned_data.get('limite_disponivel')

        if not (1 <= dia_corte <= 31):
            raise forms.ValidationError('Dia de corte deve estar entre 1 e 31')

        if not (1 <= dia_vencimento <= 31):
            raise forms.ValidationError('Dia de vencimento deve estar entre 1 e 31')

        if limite_disponivel > limite:
            raise forms.ValidationError('Limite disponível não pode ser maior que o limite total')

        return cleaned_data


class PermissaoFinanceiraForm(forms.ModelForm):
    class Meta:
        model = PermissaoFinanceira
        fields = [
            'pode_criar_movimentacao', 'pode_editar_movimentacao',
            'pode_excluir_movimentacao', 'pode_ver_todas_movimentacoes',
            'pode_gerenciar_cartoes', 'pode_gerenciar_usuarios'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
