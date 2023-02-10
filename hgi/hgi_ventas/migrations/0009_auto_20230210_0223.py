# Generated by Django 3.2.16 on 2023-02-10 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hgi_users', '0001_initial'),
        ('hgi_static', '0007_alter_contrato_tipo'),
        ('hgi_ventas', '0008_prodrecurso_recurso'),
    ]

    operations = [
        migrations.CreateModel(
            name='CajaChica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('aut', models.IntegerField()),
                ('total', models.IntegerField()),
                ('contrato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_static.contrato')),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=30, null=True)),
                ('operacion', models.IntegerField(blank=True, null=True)),
                ('nco', models.CharField(blank=True, max_length=3, null=True)),
                ('orden_1', models.IntegerField(blank=True, null=True)),
                ('orden_2', models.IntegerField(blank=True, null=True)),
                ('orden_3', models.IntegerField(blank=True, null=True)),
                ('iva', models.BooleanField(default=True)),
                ('ret', models.IntegerField(blank=True, null=True)),
                ('referencia', models.CharField(blank=True, max_length=30, null=True)),
                ('fim', models.CharField(blank=True, max_length=2, null=True)),
                ('lve', models.IntegerField(blank=True, null=True)),
                ('olv', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='prodrecurso',
            name='partida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.partida'),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='afe',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='ant',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='car',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='doc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='ing',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='lso',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='mat',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productooc',
            name='moc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='arr',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='cch',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='col',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='man',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='nco',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='ope',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='pag',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='pro',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='rah',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='rem',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tipooc',
            name='sub',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ItemRecurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, max_length=80, null=True)),
                ('sca', models.CharField(blank=True, max_length=25, null=True)),
                ('unidad', models.CharField(blank=True, max_length=10, null=True)),
                ('cantidad', models.FloatField()),
                ('precio', models.IntegerField()),
                ('observacion', models.CharField(blank=True, max_length=500, null=True)),
                ('activo', models.BooleanField(default=False)),
                ('ing', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('contrato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_static.contrato')),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('partida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.partida')),
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.prodrecurso')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCajaChica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalle', models.CharField(blank=True, max_length=70, null=True)),
                ('orden', models.IntegerField()),
                ('total', models.IntegerField()),
                ('ie', models.IntegerField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('caja_chica', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.cajachica')),
                ('contrato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_static.contrato')),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('partida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.partida')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_users.proveedor')),
                ('recurso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.prodrecurso')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.tipodocumento')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCajaChica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('oba', models.CharField(blank=True, max_length=15, null=True)),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cajachica',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_ventas.estadocajachica'),
        ),
        migrations.AddField(
            model_name='cajachica',
            name='oc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hgi_ventas.ordencompra'),
        ),
    ]