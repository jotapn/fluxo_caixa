from django import forms
from .models import Cadastro, Endereco, Atributo

class CadastroForm(forms.ModelForm):
    atributos = forms.ModelMultipleChoiceField(
        queryset=Atributo.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Exibe opções como checkboxes
        required=True,
        label="Atributos",
        help_text="Selecione um ou mais papéis para este cadastro (Cliente, Fornecedor, Colaborador)."
    )
     # Campos relacionados ao endereço
    cep = forms.CharField(max_length=9, label="CEP", required=True)
    logradouro = forms.CharField(max_length=100, label="Endereço", required=True)
    numero = forms.CharField(max_length=10, label="Número", required=True)
    complemento = forms.CharField(max_length=40, required=False, label="Complemento")
    referencia = forms.CharField(max_length=100, required=False, label="Referência")
    bairro = forms.CharField(max_length=50, label="Bairro", required=True)
    municipio = forms.CharField(max_length=50, label="Município", required=True)
    estado = forms.CharField(max_length=2, label="Estado", required=True)
    pais = forms.CharField(max_length=20, label="País", required=True, initial="Brasil")

    class Meta:
        model = Cadastro
        fields = [
            'nome',
            'nome_fantasia',
            'tipo_pessoa',
            'cnpj_cpf',
            'email',
            'telefone',
            'atributos',
            'cep', 'logradouro', 'numero', 'complemento',
            'referencia', 'bairro', 'municipio', 'estado', 'pais',
        ]
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_cnpj_cpf(self):
        # Validação adicional para CPF/CNPJ
        cnpj_cpf = self.cleaned_data.get('cnpj_cpf')
        # A validação já foi implementada no modelo, mas podemos adicionar mensagens personalizadas aqui
        if not cnpj_cpf:
            raise forms.ValidationError("O campo CPF/CNPJ é obrigatório.")
        return cnpj_cpf

    def save(self, commit=True):
        # Salvando o endereço associado ao cadastro
        instance = super().save(commit=False)

        # Criar ou atualizar o endereço
        endereco = Endereco(
            cep=self.cleaned_data.get('cep'),
            logradouro=self.cleaned_data.get('logradouro'),
            numero=self.cleaned_data.get('numero'),
            complemento=self.cleaned_data.get('complemento'),
            referencia=self.cleaned_data.get('referencia'),
            bairro=self.cleaned_data.get('bairro'),
            municipio=self.cleaned_data.get('municipio'),
            estado=self.cleaned_data.get('estado'),
            pais=self.cleaned_data.get('pais'),
        )
        if commit:
            endereco.save()
            instance.endereco = endereco
            instance.save()
            # Salvar os atributos selecionados
            self.cleaned_data['atributos'].update(cadastros=instance)
        return instance