# Generated by Django 5.1.1 on 2024-11-14 01:21

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bancos', '0003_alter_banco_status_alter_contabancaria_agencia_and_more'),
        ('clientes', '0002_remove_cliente_xpto'),
        ('operacoes', '0003_remove_operacoes_xpto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('tipo_transacao', models.CharField(choices=[('RE', 'Receita'), ('DE', 'Despesa'), ('IV', 'Investimento'), ('TC', 'Transferência entre contas')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Movimentacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('data', models.DateField()),
                ('situacao', models.CharField(choices=[('PG', 'Pago'), ('AP', 'A pagar')], default='AP', max_length=2)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bancos.contabancaria')),
                ('tipo_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagamentos', to='operacoes.tipopagamento')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Valor')),
                ('tipo_transacao', models.CharField(choices=[('RE', 'Receita'), ('DE', 'Despesa'), ('IV', 'Investimento'), ('TC', 'Transferência entre contas')], max_length=2)),
                ('data', models.DateField(default=datetime.datetime.now)),
                ('situacao', models.CharField(choices=[('PG', 'Pago'), ('AP', 'A pagar')], default='AP', max_length=2)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacao_categoria', to='transacoes.categoria')),
                ('metodo_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacao_pagamento', to='operacoes.tipopagamento')),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('movimentacoes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transacoes.movimentacoes')),
                ('cliente', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
                ('tipo_receita', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receitas', to='operacoes.tiporeceita')),
            ],
            bases=('transacoes.movimentacoes',),
        ),
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('movimentacoes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transacoes.movimentacoes')),
                ('tipo_despesa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='despesas', to='operacoes.tipodespesa')),
            ],
            bases=('transacoes.movimentacoes',),
        ),
    ]