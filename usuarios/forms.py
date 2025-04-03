from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cadastro.models import Pessoa


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'ativo', 'pessoa', 'is_staff', 'is_superuser']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra apenas colaboradores sem usuário vinculado
        self.fields['pessoa'].queryset = Pessoa.objects.filter(
            atributos__contains=['CO'],  # Apenas colaboradores
            usuario_pessoa__isnull=True  # Apenas quem não tem usuário
        )

    def clean_password1(self):
        """
        Define a senha baseada no CPF/CNPJ da pessoa.
        """
        pessoa = self.cleaned_data.get("pessoa")
        if pessoa and pessoa.cnpj_cpf:
            senha = pessoa.cnpj_cpf.replace(".", "").replace("-", "").replace("/", "")[:8]  # 8 primeiros dígitos
        else:
            senha = "12345678"  # Senha padrão caso não tenha CPF/CNPJ

        return senha  # Retorna a senha para ser usada pelo Django

    def clean_pessoa(self):
        """Valida se a pessoa selecionada realmente atende aos critérios"""
        pessoa = self.cleaned_data.get('pessoa')
        if pessoa and ('CO' not in pessoa.atributos or hasattr(pessoa, "usuario_pessoa")):
            raise forms.ValidationError("Apenas colaboradores sem usuário podem ser selecionados.")
        return pessoa
    
    def save(self, commit=True):
        """
        Garante que a senha seja setada corretamente ao salvar o usuário.
        """
        user = super().save(commit=False)
        senha = self.clean_password1()  # Obtém a senha processada
        user.set_password(senha)  # Define a senha corretamente

        if commit:
            user.save()
        return user