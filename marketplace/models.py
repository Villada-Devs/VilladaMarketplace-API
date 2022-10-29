from django.db import models
from django.db.models.fields import CharField, SlugField, DateTimeField, TextField, DateField, IntegerField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.html import format_html
from datetime import datetime, timedelta, date
from phonenumber_field.modelfields import PhoneNumberField


high_school_courses = (
    ('---', '---'),
    ('1 Año', '1 Año'),
    ('2 Año', '2 Año'),
    ('3 Año', '3 Año'),
    ('4 Año', '4 Año'),
    ('5 Año', '5 Año'),
    ('6 Año', '6 Año'),
    ('7 Año', '7 Año'),
)

product_status = (
    ('---', '---'),
    ('Usado', 'Usado'),
    ('Casi nuevo', 'Casi nuevo'),
    ('Excelente', 'Excelente')
)

size_clothing = (
    ('---', '---'),
    ('XXS', 'XXS'),
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('XXXL', 'XXXL'),
)



class Creacion(models.Model):
    product_name = models.CharField(max_length=60)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    published_date = models.DateField(blank=True, null=True)
    checked = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    tel = PhoneNumberField(blank = False)
    status = models.CharField(max_length=15, choices= product_status)

    


    class Meta:
        abstract = True
        ordering = ['-published_date', '-creation_date']






# LIBROS

class Book(Creacion):
    author = models.CharField(max_length=60, blank=True, null=True, default= '-')
    subject = models.CharField(max_length=60, blank=True, null=True, default='-')
    course = models.CharField(max_length=15, choices= high_school_courses)
    editorial = models.CharField(max_length=60, blank=True, null=True, default= '-') 

    def _str_(self):
        return f"{self.product_name} - {self.course}"

    

    @property
    def imagesbook(self):
        return self.imagesbook_set.all()

        

class ImagesBook(models.Model):
    image = models.ImageField(upload_to= "images")
    book = models.ForeignKey('Book',related_name='imagesbook', on_delete=models.CASCADE)


    def _str_(self):
        return '%s: %s' % (self.image, self.book)





# ROPA y UNIFORME

class Clothing(Creacion):
    size = models.CharField(max_length=10, choices=size_clothing, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default= '-')

    def _str_(self):
        return f"{self.product_name} - {self.size}"
    
    @property
    def imagescloth(self):
        return self.imagescloth_set.all()


class ImagesClothing(models.Model):
    image = models.ImageField(upload_to= "images")
    cloth = models.ForeignKey('Clothing',related_name='imagescloth', on_delete=models.CASCADE)


    def _str_(self):
        return f"{self.image} - {self.cloth}"


# HERRAMIENTAS

class Tool(Creacion):
    description = models.TextField(blank=True, null=True, default= '-')

    def _str_(self):
        return f"{self.product_name}"
    
    @property
    def imagestool(self):
        return self.imagestool_set.all()


class ImagesTool(models.Model):
    image = models.ImageField(upload_to= "images")
    tool = models.ForeignKey('Tool',related_name='imagestool', on_delete=models.CASCADE)


    def _str_(self):
        return f"{self.image} - {self.tool}"