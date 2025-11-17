from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import New, Suggestion

class NewAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(mce_attrs={
        'height': 400,
        'menubar': True,
        'plugins': 'link image code table lists',
        'toolbar': 'undo redo | formatselect | bold italic backcolor | \
                    alignleft aligncenter alignright alignjustify | \
                    bullist numlist outdent indent | removeformat | help',
    }))

    class Meta:
        model = New
        fields = '__all__'

class SuggestionInline(admin.TabularInline):  # o admin.StackedInline si preferís más detalle
    model = Suggestion
    extra = 0  # No mostrar filas vacías por defecto
    fields = ('title', 'direction', 'description', 'symbol', 'date')
    readonly_fields = ()  # Podés agregar campos no editables si querés
    show_change_link = True 

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    form = NewAdminForm
    list_display = ('title', 'date')
    fields = ('title', 'subtitle', 'content', 'image', 'date')
    search_fields = ('title', 'subtitle')
    list_filter = ('date',)
    inlines = [SuggestionInline]