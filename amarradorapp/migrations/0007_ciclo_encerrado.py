# Generated by Django 5.0.4 on 2024-06-20 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarradorapp', '0006_gasto_excluido_alter_ciclo_valor_alter_gasto_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclo',
            name='encerrado',
            field=models.BooleanField(default=False),
        ),
    ]
