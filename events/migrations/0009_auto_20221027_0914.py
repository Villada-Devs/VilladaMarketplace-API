# Generated by Django 3.2.13 on 2022-10-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_event_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('Bienvenida a familias de primer año', 'Bienvenida a familias de primer año'), ('Talleres pedagógicos', 'Talleres pedagógicos'), ('Conferencias', 'Conferencias'), ('Retiros espirituales', 'Retiros espirituales'), ('Integración de los padres a la labor educativa', 'Integración de los padres a la labor educativa'), ('Locro del exalumno salesiano del villada', 'Locro del exalumno salesiano del villada'), ('UPF solidaria', 'UPF solidaria'), ('Dia del educador', 'Dia del educador'), ('Bicicleteada salesiana', 'Bicicleteada salesiana'), ('Asado de fin de año', 'Asado de fin de año'), ('Valle de la inmaculada', 'Valle de la inmaculada')], max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='short_description',
            field=models.CharField(max_length=200),
        ),
    ]
