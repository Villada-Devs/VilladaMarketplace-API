from django.db import models
from django.db.models.fields import CharField, SlugField, DateTimeField, TextField, DateField, IntegerField
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.html import format_html
from datetime import datetime, timedelta, date


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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    published_date = models.DateField(blank=True, null=True)
    checked = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    tel = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices= product_status)

    



    class Meta:
        abstract = True






# LIBROS

class Book(Creacion):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=60, blank=True, null=True)
    subject = models.CharField(max_length=60)
    course = models.CharField(max_length=15, choices= high_school_courses)
    editorial = models.CharField(max_length=60, blank=True, null=True) 

    def __str__(self):
        return f"{self.title} - {self.course}"

    # def titulo(self):

    #     hoy = date.today()
    #     limit_days = hoy - self.creation_date # nose por que en ves de poner hoy si pongo todo 'date.today()' no funciona asi que lo dejo asi
    #     print(limit_days, timedelta(weeks=2))


    #     if limit_days > timedelta(weeks=2):
    #         return format_html('<span style="color: red;">{0}</span>'.format(self.title))
    #     if self.checked == False:
    #         return format_html('<span style="color: yellow;">{0}</span>'.format(self.title)) # esto hace que se ponga de un color o otro el 'title' si esta checkeado o no
    #     else:
    #         return format_html('<span style="color: green;">{0}</span>'.format(self.title))

    @property
    def imagesbook(self):
        return self.imagesbook_set.all()

        

class ImagesBook(models.Model):
    image = models.ImageField(upload_to= "images")
    book = models.ForeignKey('Book',related_name='imagesbook', on_delete=models.CASCADE)


    def __str__(self):
        return '%s: %s' % (self.image, self.book)





# ROPA y UNIFORME

class Clothing(Creacion):
    type_of_cloth = models.CharField(max_length=60)
    size = models.CharField(max_length=10, choices=size_clothing, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type_of_cloth} - {self.size}"
    
    @property
    def imagescloth(self):
        return self.imagescloth_set.all()


class ImagesClothing(models.Model):
    image = models.ImageField(upload_to= "images")
    cloth = models.ForeignKey('Clothing',related_name='imagescloth', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.image} - {self.cloth}"


# HERRAMIENTAS

class Tool(Creacion):
    tool = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tool}"
    
    @property
    def imagestool(self):
        return self.imagestool_set.all()


class ImagesTool(models.Model):
    image = models.ImageField(upload_to= "images")
    tool = models.ForeignKey('Tool',related_name='imagestool', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.image} - {self.tool}"
