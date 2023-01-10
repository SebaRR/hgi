# Generated by Django 3.2.16 on 2023-01-10 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_users', '0003_rename_owner_usertoken_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('romanNumber', models.CharField(default='', max_length=5)),
                ('number', models.IntegerField(default=1)),
                ('abbreviation', models.CharField(default='', max_length=2)),
            ],
            options={
                'verbose_name': 'Región',
                'verbose_name_plural': 'Regiones',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('commune', models.CharField(max_length=100)),
                ('activity', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('country', models.CharField(choices=[('Chile', 'Chile'), ('Argentina', 'Argentina')], default='Chile', max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_users.city')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hgi_users.region')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hgi_users.region'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='city',
            order_with_respect_to='region',
        ),
    ]
