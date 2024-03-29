# Generated by Django 3.2.16 on 2023-01-30 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_static', '0004_alter_obra_creador'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoObra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='obra',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_static.estadoobra'),
        ),
    ]
