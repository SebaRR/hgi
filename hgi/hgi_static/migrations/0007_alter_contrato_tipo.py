# Generated by Django 3.2.16 on 2023-02-03 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_static', '0006_auto_20230131_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='tipo',
            field=models.ForeignKey(default=6, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_static.tipocontrato'),
        ),
    ]
