# Generated by Django 5.1.1 on 2024-10-10 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_campana_presupuesto_campana_tamaño_audiencia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='fecha_finalizacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
