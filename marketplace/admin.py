from atexit import register
from django.contrib import admin
from .models import *
from datetime import datetime, timedelta, date



admin.site.disable_action('delete_selected') #desactivamos accion del admin

 #  IMAGENES DE LIBROS
class ImagesBookAdmin(admin.TabularInline):
    model=ImagesBook

    

class BookAdmin(admin.ModelAdmin):
    inlines = [ImagesBookAdmin]
    readonly_fields = ('checked', 'published_date',)
    list_display = ['title','id', 'subject', 'course', 'checked','creation_date','published_date' ]
    ordering = ['checked','creation_date',] 
    list_display_links = ['title']
    list_filter = ['checked',]
    actions = ['check_books',]
    

    def check_books(self, request, queryset):
        for book in queryset:
            if book.published_date == None:

                book.checked = True # TODOS los que recibio de la query les pone 'checked' = True
                book.published_date = date.today()
                book.save()

            else:
                return book

    
    

"""fieldsets = (
        (None,{
            'fields':('id','title', 'subject', 'course', 'author', 'editorial','tel','created_by',)
        }),
    )
"""


    

# IMAGENES DE ROPA
class ImagesClothingAdmin(admin.TabularInline):
    model=ImagesClothing

class ClothingAdmin(admin.ModelAdmin):
    inlines = [ImagesClothingAdmin,]
    readonly_fields = ('checked', 'published_date',)
    list_display = ['type_of_cloth','id', 'checked','creation_date','published_date' ]
    ordering = ['checked','creation_date',] 
    list_display_links = ['type_of_cloth']
    list_filter = ['checked',]
    actions = ['check_cloths',]
    


   


    def check_cloths(self, request, queryset):
        for cloth in queryset:
            if cloth.published_date == None:

                cloth.checked = True # TODOS los que recibio de la query les pone 'checked' = True
                cloth.published_date = date.today()
                cloth.save()

            else:
                return cloth

    
    

"""fieldsets = (
        (None,{
            'fields':('id','type_of_cloth', 'size', 'description','tel','created_by',)
        }),
    )   
"""


#   IMAGENES DE HERRAMIENTAS
class ImagesToolAdmin(admin.TabularInline):
    model=ImagesTool

class ToolAdmin(admin.ModelAdmin):
    inlines = [ImagesToolAdmin,]
    readonly_fields = ('checked', 'published_date',)
    list_display = ['tool','id', 'checked','creation_date','published_date' ]
    ordering = ['checked','creation_date',] 
    list_display_links = ['tool']
    list_filter = ['checked',]
    actions = ['check_tools',]
    


   


    def check_tools(self, request, queryset):
        for tool in queryset:
            if tool.published_date == None:

                tool.checked = True # TODOS los que recibio de la query les pone 'checked' = True
                tool.published_date = date.today()
                tool.save()

            else:
                return tool

    
    

""" fieldsets = (
        (None,{
            'fields':('id','tool', 'description','tel','created_by',)
        }),
    )
    """





admin.site.register(Book, BookAdmin)
admin.site.register(ImagesBook)

admin.site.register(Clothing, ClothingAdmin )
admin.site.register(ImagesClothing)

admin.site.register(Tool, ToolAdmin)
admin.site.register(ImagesTool)

