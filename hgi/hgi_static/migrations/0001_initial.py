# Generated by Django 3.2.16 on 2023-01-26 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClasiContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('abreviatura', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=9)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('par', models.BooleanField(default=False)),
                ('mat', models.BooleanField(default=False)),
                ('mau', models.BooleanField(default=False)),
                ('auo', models.BooleanField(default=False)),
                ('proa', models.BooleanField(default=False)),
                ('oc', models.BooleanField(default=False)),
                ('vis', models.BooleanField(default=False)),
                ('uf', models.FloatField()),
                ('sa', models.IntegerField(default=0)),
                ('m2', models.IntegerField(null=True)),
                ('peso', models.IntegerField(null=True)),
                ('ccp', models.IntegerField(default=0)),
                ('mon', models.IntegerField()),
                ('pro', models.IntegerField()),
                ('inicio', models.DateTimeField(auto_now_add=True)),
                ('termino', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('abreviatura', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoOC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('orden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=20)),
                ('simbolo', models.CharField(max_length=3)),
                ('dec', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=6)),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('creador', models.CharField(max_length=25)),
                ('fecha', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('abreviatura', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('dias', models.IntegerField()),
                ('orden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoPresupuesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=30)),
                ('diminutivo', models.CharField(max_length=3)),
                ('operacion', models.IntegerField()),
                ('orden', models.IntegerField()),
            ],
        ),
    ]