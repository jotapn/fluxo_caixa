from django import template

register = template.Library()

@register.filter
def moeda(valor):
    """Formata um número como moeda brasileira (R$)."""
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
