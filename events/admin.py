from django.contrib import admin
<<<<<<< HEAD
from .models import Event, ImagesEvent
# Register your models here.


class ImagesBookAdmin(admin.TabularInline):
    model=ImagesEvent


class EventAdmin(admin.ModelAdmin):
    inlines = [ImagesBookAdmin]



admin.site.register(Event, EventAdmin)
=======

from .models import Event
# Register your models here.


admin.site.register(Event)
>>>>>>> pagination-market
