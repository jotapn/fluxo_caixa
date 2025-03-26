from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("id", "username", "email", "ativo", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "ativo")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = (
        ("Dados do Usuário", {"fields": ("username", "password", "email", "ativo", "pessoa")}),
        ("Permissões", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Criar Novo Usuário",
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "ativo", "pessoa" , "is_staff", "is_superuser"),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)