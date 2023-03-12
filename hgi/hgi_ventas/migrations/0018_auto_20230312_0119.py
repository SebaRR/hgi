# Generated by Django 3.2.16 on 2023-03-12 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_static', '0009_auto_20230310_0013'),
        ('hgi_ventas', '0017_alter_productooc_recurso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrecurso',
            name='contrato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hgi_static.contrato'),
        ),
        migrations.AlterField(
            model_name='itemrecurso',
            name='ing',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='itemrecurso',
            name='partida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hgi_ventas.partida'),
        ),
    ]
