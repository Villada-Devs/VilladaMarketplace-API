# Generated by Django 3.2.13 on 2022-08-09 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiauth', '0006_pool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Pool',
        ),
    ]
