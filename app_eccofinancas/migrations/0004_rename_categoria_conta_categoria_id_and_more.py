# Generated by Django 4.2.4 on 2023-10-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_eccofinancas', '0003_conta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conta',
            old_name='categoria',
            new_name='categoria_id',
        ),
        migrations.AddField(
            model_name='conta',
            name='data_vencimento_inicial',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conta',
            name='parcelas_pagas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='conta',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='conta',
            name='valor_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='numero_parcelas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
