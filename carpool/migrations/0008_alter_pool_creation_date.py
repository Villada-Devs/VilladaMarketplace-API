# Generated by Django 3.2.13 on 2022-10-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0007_pool_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]