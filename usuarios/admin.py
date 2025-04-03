from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ("id", "pessoa", "username", "ativo", "is_staff", "is_superuser")
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
                # "classes": ("wide",),
                "fields": ("username", "ativo", "pessoa", "is_staff", "is_superuser"),
            },
        ),
    )
    logger.info(f"Gerando senha p")


admin.site.register(CustomUser, CustomUserAdmin)