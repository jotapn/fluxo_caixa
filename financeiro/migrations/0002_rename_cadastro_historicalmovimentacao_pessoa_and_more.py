# Generated by Django 5.1.1 on 2025-02-21 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalmovimentacao',
            old_name='cadastro',
            new_name='pessoa',
        ),
        migrations.RenameField(
            model_name='movimentacao',
            old_name='cadastro',
            new_name='pessoa',
        ),
    ]
