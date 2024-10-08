# Generated by Django 5.1.1 on 2024-10-09 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDespesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoReceita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('AT', 'Ativo'), ('IN', 'Inativo')], default='AT', max_length=10)),
            ],
        ),
    ]
