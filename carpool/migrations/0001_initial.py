# Generated by Django 3.2.13 on 2022-08-09 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.CharField(max_length=70)),
                ('neighborhood', models.CharField(max_length=70)),
                ('slots', models.PositiveIntegerField()),
                ('day_lunes', models.BooleanField(default=False)),
                ('day_martes', models.BooleanField(default=False)),
                ('day_miercoles', models.BooleanField(default=False)),
                ('day_jueves', models.BooleanField(default=False)),
                ('day_viernes', models.BooleanField(default=False)),
                ('first_tel', models.PositiveIntegerField()),
                ('alternative_tel', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]