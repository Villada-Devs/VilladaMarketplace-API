# Generated by Django 3.2.13 on 2022-10-29 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_auto_20221002_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='clothing',
            old_name='type_of_cloth',
            new_name='product_name',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='tool',
            new_name='product_name',
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, default='-', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='editorial',
            field=models.CharField(blank=True, default='-', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='subject',
            field=models.CharField(blank=True, default='-', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='description',
            field=models.TextField(blank=True, default='-', null=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='description',
            field=models.TextField(blank=True, default='-', null=True),
        ),
    ]