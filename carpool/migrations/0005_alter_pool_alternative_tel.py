# Generated by Django 3.2.13 on 2022-10-02 23:58

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0004_alter_pool_first_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='alternative_tel',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
