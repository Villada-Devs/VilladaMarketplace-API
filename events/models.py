
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

event_types = (
    ('BIENVENIDA A FAMILIAS DE PRIMER ' ,'Bienvenida a familias de primer año'),
    ('TALLERES PEDAGÓGICOS' ,'Talleres pedagógicos'),
    ('CONFERENCIAS' ,'Conferencias'),
    ('RETIROS ESPIRITUALES' ,'Retiros espirituales'),
    ('INTEGRACION DE LOS PADRES A LA LABOR EDUCATIVA' ,'Integración de los padres a la labor educativa'),
    ('LOCRO DEL EXALUMNO SALESIANO DEL VILLADA', 'Locro del exalumno salesiano del villada'),
    ('UPF SOLIDARIA', 'UPF solidaria'),
    ('DIA DEL EDUCADOR', 'Dia del educador'),
    ('BICICLETEADA SALESIANA', 'Bicicleteada salesiana'),
    ('ASADO DE FIN DE AÑO', 'Asado de fin de año'),
    ('VALLE DE LA INMACULADA', 'Valle de la inmaculada'),
)
class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    short_description = models.CharField(max_length=80)
    created_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length = 50, choices = event_types)

    def __str__(self):
        return self.title 
    class Meta:
        ordering = ['-created_date']

    

    @property
    def imagesevent(self):
        return self.imagesbook_set.all()

class ImagesEvent(models.Model):
    image = models.ImageField(upload_to= "images")
    event = models.ForeignKey('Event',related_name='imagesevent', on_delete=models.CASCADE)



    def __str__(self):
        return '%s: %s' % (self.image, self.event)

