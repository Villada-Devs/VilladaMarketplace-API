
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

event_types = (
    ('Bienvenida a familias de primer año' ,'Bienvenida a familias de primer año'),
    ('Talleres pedagógicos' ,'Talleres pedagógicos'),
    ('Conferencias' ,'Conferencias'),
    ('Retiros espirituales' ,'Retiros espirituales'),
    ('Integración de los padres a la labor educativa' ,'Integración de los padres a la labor educativa'),
    ('Locro del exalumno salesiano del villada', 'Locro del exalumno salesiano del villada'),
    ('UPF solidaria', 'UPF solidaria'),
    ('Dia del educador', 'Dia del educador'),
    ('Bicicleteada salesiana', 'Bicicleteada salesiana'),
    ('Asado de fin de año', 'Asado de fin de año'),
    ('Valle de la inmaculada', 'Valle de la inmaculada'),
)
class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    short_description = models.CharField(max_length=200)
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

