# Generated by Django 5.1.1 on 2025-03-12 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancos', '0003_remove_contabancaria_gerente_banco_codigo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco',
            name='codigo',
        ),
        migrations.AddField(
            model_name='banco',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='bancos/logos/', verbose_name='Logo do Banco'),
        ),
        migrations.AddField(
            model_name='contabancaria',
            name='cartao_credito',
            field=models.BooleanField(default=False),
        ),
    ]
