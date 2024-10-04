# Generated by Django 5.1.1 on 2024-10-01 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0004_rename_clientes_cliente_rename_cnpj_cliente_cnpj_cpf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('saldo_inicial', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('tipo', models.CharField(choices=[('pagamento', 'Tipo de Pagamento'), ('despesa', 'Tipo de Despesa'), ('entrada', 'Tipo de Entrada')], max_length=10)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('data', models.DateField(auto_now_add=True)),
                ('situacao', models.CharField(choices=[('PG', 'Pago'), ('AP', 'A PAGAR')], max_length=2)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimentacoes.banco')),
                ('tipo_despesa', models.ForeignKey(limit_choices_to={'tipo': 'despesa'}, on_delete=django.db.models.deletion.PROTECT, related_name='despesas_saida', to='movimentacoes.tipo')),
                ('tipo_pagamento', models.ForeignKey(limit_choices_to={'tipo': 'pagamento'}, on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='movimentacoes.tipo')),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('data', models.DateField(auto_now_add=True)),
                ('situacao', models.CharField(choices=[('PG', 'Pago'), ('AP', 'A PAGAR')], max_length=2)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimentacoes.banco')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
                ('tipo_entrada', models.ForeignKey(limit_choices_to={'tipo': 'entrada'}, on_delete=django.db.models.deletion.PROTECT, related_name='entradas', to='movimentacoes.tipo')),
                ('tipo_pagamento', models.ForeignKey(limit_choices_to={'tipo': 'pagamento'}, on_delete=django.db.models.deletion.PROTECT, related_name='pagamentos', to='movimentacoes.tipo')),
            ],
        ),
    ]