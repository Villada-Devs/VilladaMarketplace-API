# Generated by Django 3.2.13 on 2022-10-02 23:51

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0002_alter_pool_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='first_tel',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]
