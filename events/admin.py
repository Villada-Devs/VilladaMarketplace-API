from django.contrib import admin
from .models import Event, ImagesEvent
# Register your models here.


class ImagesBookAdmin(admin.TabularInline):
    model=ImagesEvent


class EventAdmin(admin.ModelAdmin):
    inlines = [ImagesBookAdmin]



admin.site.register(Event, EventAdmin)
