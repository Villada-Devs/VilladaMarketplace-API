from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images")
    event_date = models.DateTimeField()


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
    first_tel = models.PositiveIntegerField()
    alternative_tel = models.PositiveIntegerField()