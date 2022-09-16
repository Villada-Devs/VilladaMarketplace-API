from django.contrib import admin

from .models import Pool



class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('checked', 'published_date')
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

admin.site.register(Pool)