
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField()
    short_description = models.CharField(max_length=80)
    created_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()

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

