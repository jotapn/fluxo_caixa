# movimentacoes/celery.py

from celery import shared_task
import pandas as pd
from .models import Entrada, Saida

@shared_task
def importar_entradas_task(file_path):
    # Lê a planilha de entradas
    try:
        data = pd.read_excel(file_path)
        
        # Itera sobre as linhas e cria entradas no banco de dados
        for _, row in data.iterrows():
            Entrada.objects.create(
                cliente=row['Cliente'],
                descricao=row['Descrição'],
                valor=row['Valor'],
                data=row['Data'],
                banco=row['Banco'],
                tipo_pagamento=row['Tipo de Pagamento'],
                tipo_entrada=row['Tipo de Entrada'],
                situacao=row['Situação']
            )
        return 'Importação de entradas concluída com sucesso!'
    except Exception as e:
        return f'Erro na importação de entradas: {e}'

@shared_task
def importar_saidas_task(file_path):
    # Lê a planilha de saídas
    try:
        data = pd.read_excel(file_path)
        
        # Itera sobre as linhas e cria saídas no banco de dados
        for _, row in data.iterrows():
            Saida.objects.create(
                tipo_despesa=row['Tipo de Despesa'],
                descricao=row['Descrição'],
                valor=row['Valor'],
                data=row['Data'],
                banco=row['Banco'],
                tipo_pagamento=row['Tipo de Pagamento'],
                situacao=row['Situação']
            )
        return 'Importação de saídas concluída com sucesso!'
    except Exception as e:
        return f'Erro na importação de saídas: {e}'
