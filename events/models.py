from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images")
    event_date = models.DateTimeField()

    class Meta:
        ordering = ['-created_date']