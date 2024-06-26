# Generated by Django 5.0.6 on 2024-05-12 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('senha', models.CharField(max_length=64)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Usuário',
            },
        ),
    ]
