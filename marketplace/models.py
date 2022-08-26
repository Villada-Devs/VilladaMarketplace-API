from django.db import models
from django.db.models.fields import CharField, SlugField, DateTimeField, TextField, DateField, IntegerField
from django.contrib.auth.models import User
from django.conf import settings


high_school_years = (
    ('1° Año', '1° Año'),
    ('2° Año', '2° Año'),
    ('3° Año', '3° Año'),
    ('4° Año', '4° Año'),
    ('5° Año', '5° Año'),
    ('6° Año', '6° Año'),
    ('7° Año', '7° Año'),
)

product_status = (
    ('Usado', 'Usado'),
    ('Casi nuevo', 'Casi nuevo'),
    ('Excelente', 'Excelente')
)

size_clothing = (
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    on_circulation = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    tel = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices= product_status)



    class Meta:
        abstract = True


# LIBROS

class Book(Creacion):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60, blank=True, null=True)
    matter = models.CharField(max_length=60)
    age = models.CharField(max_length=15, choices= high_school_years)
    editorial = models.CharField(max_length=60, blank=True, null=True) 

    def __str__(self):
        return f"{self.title} - {self.age}"


class ImagesBook(models.Model):
    image = models.ImageField(upload_to= "images")
    book = models.ForeignKey('Book',related_name='imagesbook', on_delete=models.CASCADE)


    def __str__(self):
        return '%s: %s' % (self.image, self.book)



# ROPA y UNIFORME

class Clothing(Creacion):
    type_of_garment = models.CharField(max_length=60)
    size = models.CharField(max_length=10, choices=size_clothing, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.type_of_garment} - {self.size}"


class ImagesClothing(models.Model):
    image = models.ImageField(upload_to= "images")
    cloth = models.ForeignKey('Clothing',related_name='imagescloth', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.image} - {self.cloth}"


# HERRAMIENTAS

class Tool(Creacion):
    tool = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return f"{self.tool}"


class ImagesTool(models.Model):
    image = models.ImageField(upload_to= "images")
    tool = models.ForeignKey('Tool',related_name='imagestool', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.image} - {self.tool}"
