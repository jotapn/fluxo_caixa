from bancos.models import Banco

# Lista de bancos populares (sem código)
BANCOS_POPULARES = [
    "Banco do Brasil",
    "Bradesco",
    "Itaú Unibanco",
    "Caixa Econômica Federal",
    "Santander",
    "Banco Safra",
    "Banco Inter",
    "BTG Pactual",
    "Nubank",
    "C6 Bank",
    "Neon",
    "Original",
    "Banco PAN",
    "Sicoob",
    "Sicredi",
    "Banco BMG",
    "Banco Votorantim",
    "Banco Mercantil do Brasil",
    "Banco da Amazônia",
    "Banco do Nordeste",
    "PagBank (PagSeguro)",
    "Banco BS2",
    "Banco Digio",
    "Banco ModalMais",
]

def criar_bancos():
    """Cria bancos populares se ainda não existirem"""
    for nome in BANCOS_POPULARES:
        banco, criado = Banco.objects.get_or_create(nome=nome)
        if criado:
            print(f"✅ Banco criado: {banco.nome}")
        else:
            print(f"🔄 Banco já existente: {banco.nome}")

if __name__ == "__main__":
    criar_bancos()