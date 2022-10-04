from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Pool(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    locality = models.CharField(max_length=70)
    neighborhood = models.CharField(max_length=70)
    slots = models.PositiveIntegerField()
    day_lunes = models.BooleanField(default=False)
    day_martes = models.BooleanField(default=False)
    day_miercoles = models.BooleanField(default=False)
    day_jueves = models.BooleanField(default=False)
    day_viernes = models.BooleanField(default=False)
    first_tel = PhoneNumberField(blank=False)
    alternative_tel = PhoneNumberField(blank=False)
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)
    
    def __str__(self):
        return "pool en " + self.locality

    class Meta:
        ordering = ['-id']

