# Generated by Django 3.2.16 on 2023-02-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_ventas', '0011_alter_tipodocumento_referencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordencompra',
            name='descuento_general',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='observacion',
            field=models.CharField(default='Sin Observaciones.', max_length=500),
        ),
    ]