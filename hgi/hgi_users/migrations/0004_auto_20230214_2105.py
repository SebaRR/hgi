# Generated by Django 3.2.16 on 2023-02-15 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_users', '0003_permisocontrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='permisocontrato',
            name='modificar_ccp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permisocontrato',
            name='modificar_ccr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permisocontrato',
            name='ver_ccp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permisocontrato',
            name='ver_ccr',
            field=models.BooleanField(default=False),
        ),
    ]
