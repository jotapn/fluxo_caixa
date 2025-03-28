from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from cadastro.models import Pessoa


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'ativo', 'pessoa', 'is_staff', 'is_superuser']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra apenas colaboradores sem usuário vinculado
        self.fields['pessoa'].queryset = Pessoa.objects.filter(
            atributos__contains=['CO'],  # Apenas colaboradores
            usuario_pessoa__isnull=True  # Apenas quem não tem usuário
        )

    def clean_pessoa(self):
        """Valida se a pessoa selecionada realmente atende aos critérios"""
        pessoa = self.cleaned_data.get('pessoa')
        if pessoa and ('CO' not in pessoa.atributos or hasattr(pessoa, "usuario_pessoa")):
            raise forms.ValidationError("Apenas colaboradores sem usuário podem ser selecionados.")
        return pessoa