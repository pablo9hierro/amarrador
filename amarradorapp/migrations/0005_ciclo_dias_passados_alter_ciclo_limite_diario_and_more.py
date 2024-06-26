# Generated by Django 5.0.4 on 2024-06-10 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarradorapp', '0004_alter_ciclo_nome_gasto'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciclo',
            name='dias_passados',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='limite_diario',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='nome',
            field=models.CharField(default='Valor Padrão', max_length=100),
        ),
    ]
