from django import forms
from . models import Cliente
from validate_docbr import CPF, CNPJ

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields = '__all__'

    def clean_cnpj_cpf(self):
        cnpj_cpf = self.cleaned_data.get('cnpj_cpf')
        tipo_pessoa = self.cleaned_data.get('tipo_pessoa')

        if tipo_pessoa == 'pf':  # Valida como CPF
            cpf_validator = CPF()
            if not cpf_validator.validate(cnpj_cpf):
                raise forms.ValidationError('CPF inválido.')
        elif tipo_pessoa == 'pj':  # Valida como CNPJ
            cnpj_validator = CNPJ()
            if not cnpj_validator.validate(cnpj_cpf):
                raise forms.ValidationError('CNPJ inválido.')
        else:
            raise forms.ValidationError('Tipo de pessoa inválido.')

        return cnpj_cpf