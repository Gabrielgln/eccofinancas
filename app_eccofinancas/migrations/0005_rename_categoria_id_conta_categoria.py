# Generated by Django 4.2.4 on 2023-10-01 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_eccofinancas', '0004_rename_categoria_conta_categoria_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conta',
            old_name='categoria_id',
            new_name='categoria',
        ),
    ]
