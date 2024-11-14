def ajustar_saldo_conta(instance, sinal):
    """Ajusta o saldo da conta baseado no valor e no sinal."""
    if sinal == "-":
        instance.conta.saldo_atual -= instance.valor
    elif sinal == "+":
        instance.conta.saldo_atual += instance.valor
    instance.conta.save()

def salvar_movimentacao(instance,situacao,  tipo_operacao):
    """Lógica de ajuste de saldo para salvar nova movimentação ou alteração de situação para 'Pago'."""
    if instance.pk is None or instance.__class__.objects.get(pk=instance.pk).situacao != situacao.PAGO:
        # Ajusta o saldo se a situação for 'Pago'
        if instance.situacao == situacao.PAGO:
            sinal = "+" if tipo_operacao else "-"
            ajustar_saldo_conta(instance, sinal)
    elif instance.situacao == situacao.A_PAGAR:
        sinal = "-" if tipo_operacao else "+"
        ajustar_saldo_conta(instance, sinal)

def deletar_movimentacao(instance, situacao, tipo_operacao):
    """Lógica de ajuste de saldo para deletar movimentação paga."""
    if instance.situacao == situacao.PAGO:
        sinal = "-" if tipo_operacao else "+"
        ajustar_saldo_conta(instance, sinal)
