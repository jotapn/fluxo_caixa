# Generated by Django 5.1.1 on 2024-11-14 01:40

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0003_remove_operacoes_xpto'),
        ('transacoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transacao',
            options={'ordering': ['-data'], 'verbose_name_plural': 'Transações'},
        ),
        migrations.AddField(
            model_name='categoria',
            name='classificacao',
            field=models.CharField(blank=True, choices=[('VA', 'Variável'), ('FX', 'Fixa')], max_length=2, null=True, verbose_name='Classificação'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='status',
            field=models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='tipo_transacao',
            field=models.CharField(choices=[('RE', 'Receita'), ('DE', 'Despesa'), ('IV', 'Investimento'), ('TC', 'Transferência entre contas')], max_length=2, verbose_name='Tipo Transação'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacao_categoria', to='transacoes.categoria', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='data',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='metodo_pagamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacao_pagamento', to='operacoes.tipopagamento', verbose_name='Método Pagamento'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='situacao',
            field=models.CharField(choices=[('PG', 'Pago'), ('AP', 'A pagar')], default='AP', max_length=2, verbose_name='Situação'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='tipo_transacao',
            field=models.CharField(choices=[('RE', 'Receita'), ('DE', 'Despesa'), ('IV', 'Investimento'), ('TC', 'Transferência entre contas')], max_length=2, verbose_name='Tipo Transação'),
        ),
    ]
