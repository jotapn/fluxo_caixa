# Generated by Django 5.1.1 on 2025-02-21 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_rename_cadastro_historicalmovimentacao_pessoa_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RateioCentroDeCusto',
        ),
    ]
