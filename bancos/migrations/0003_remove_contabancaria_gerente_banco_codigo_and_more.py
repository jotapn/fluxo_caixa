# Generated by Django 5.1.1 on 2025-03-12 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0002_rename_nome_contabancaria_descricao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contabancaria',
            name='gerente',
        ),
        migrations.AddField(
            model_name='banco',
            name='codigo',
            field=models.CharField(default=1, max_length=10, unique=True, verbose_name='Código do Banco'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banco',
            name='nome',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome do Banco'),
        ),
        migrations.AlterField(
            model_name='banco',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='contabancaria',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]
