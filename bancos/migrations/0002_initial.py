# Generated by Django 5.1.1 on 2025-03-21 01:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bancos', '0001_initial'),
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicosaldo',
            name='movimentacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_saldo', to='financeiro.movimentacao'),
        ),
    ]
