# Generated by Django 4.2.4 on 2023-09-29 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_eccofinancas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.TextField(max_length=255)),
            ],
        ),
    ]
