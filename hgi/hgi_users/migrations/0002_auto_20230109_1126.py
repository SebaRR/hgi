# Generated by Django 3.2.16 on 2023-01-09 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hgi_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('validation', models.BooleanField(default=False)),
                ('recovery', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
