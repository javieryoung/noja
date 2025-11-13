from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import New

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

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    form = NewAdminForm
    list_display = ('title', 'date')
    fields = ('title', 'subtitle', 'content', 'image', 'date')
    search_fields = ('title', 'subtitle')
    list_filter = ('date',)