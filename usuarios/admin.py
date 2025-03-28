from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ("id", "username", "ativo", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "ativo")
    search_fields = ("username",)
    ordering = ("id",)

    fieldsets = (
        ("Dados do Usuário", {"fields": ("username", "ativo", "pessoa")}),
        ("Permissões", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Criar Novo Usuário",
            {
                "classes": ("wide",),
                "fields": ("username", "ativo", "pessoa" , "is_staff", "is_superuser"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):

        if not change:
            if obj.pessoa and obj.pessoa.cnpj_cpf:
                obj.pessoa.cnpj_cpf.replace(".","").replace("-", "").replace("/", "")[:8]  # Pega os 8 primeiros dígitos
            else:
                senha = "12345678"
            obj.set_password(senha)  # Define a senha no Django
            obj.save()

admin.site.register(CustomUser, CustomUserAdmin)