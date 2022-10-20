
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

event_types = (
    ('BIENVENIDA A FAMILIAS DE PRIMER AÑO' ,'BIENVENIDA A FAMILIAS DE PRIMER AÑO'),
    ('TALLERES PEDAGÓGICOS' ,'TALLERES PEDAGÓGICOS'),
    ('CONFERENCIAS' ,'CONFERENCIAS'),
    ('RETIROS ESPIRITUALES' ,'RETIROS ESPIRITUALES'),
    ('INTEGRACION DE LOS PADRES A LA LABOR EDUCATIVA' ,'INTEGRACION DE LOS PADRES A LA LABOR EDUCATIVA'),
    ('LOCRO DEL EXALUMNO SALESIANO DEL VILLADA', 'LOCRO DEL EXALUMNO SALESIANO DEL VILLADA'),
    ('UPF SOLIDARIA', 'UPF SOLIDARIA'),
    ('DIA DEL EDUCADOR', 'DIA DEL EDUCADOR'),
    ('BICICLETEADA SALESIANA', 'BICICLETEADA SALESIANA'),
    ('ASADO DE FIN DE AÑO', 'ASADO DE FIN DE AÑO'),
    ('VALLE DE LA INMACULADA', 'VALLE DE LA INMACULADA'),
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

