from django.contrib import admin
from .models import New


# Register your models here.from .models import New

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    fields = ('title', 'subtitle', 'content', 'image', 'date')
    search_fields = ('title', 'subtitle')
    list_filter = ('date',)

