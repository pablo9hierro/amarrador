# Generated by Django 5.0.4 on 2024-06-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarradorapp', '0002_ciclo_nome_ciclo_texto'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclo',
            name='limite_diario',
            field=models.IntegerField(default=0),
        ),
    ]
