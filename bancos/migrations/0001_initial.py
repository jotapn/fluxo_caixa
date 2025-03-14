# Generated by Django 5.1.1 on 2025-02-19 01:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ContaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_atual', models.DecimalField(auto_created=True, blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('nome', models.CharField(max_length=50)),
                ('conta', models.CharField(max_length=20)),
                ('agencia', models.CharField(max_length=20, verbose_name='Agência')),
                ('gerente', models.CharField(blank=True, max_length=200, null=True)),
                ('saldo_inicial', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=2)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bancos.banco')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoSaldo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('valor_anterior', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_atual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('movimento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bancos.contabancaria')),
            ],
        ),
    ]
