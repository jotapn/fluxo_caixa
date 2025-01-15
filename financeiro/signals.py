from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import FormaRecebimento

@receiver(post_migrate)
def criar_formas_recebimento_padrao(sender, **kwargs):
    if sender.name == "financeiro":  # Substitua pelo nome da sua aplicação
        formas_padrao = [
            "Dinheiro",
            "Cartão Crédito",
            "Cartão Débito",
            "Transferência (TED)",
            "PIX"
        ]
        for forma in formas_padrao:
            FormaRecebimento.objects.get_or_create(nome=forma)
