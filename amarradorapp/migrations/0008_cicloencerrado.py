# Generated by Django 5.0.4 on 2024-06-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarradorapp', '0007_ciclo_encerrado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CicloEncerrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_fim', models.DateField()),
            ],
        ),
    ]
