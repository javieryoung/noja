from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, New
from django import forms
from tinymce.widgets import TinyMCE
from .models import New, Suggestion

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'nombre', 'pais', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'pais')
    search_fields = ('email', 'nombre', 'pais')
    ordering = ('nombre',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'telefono', 'pais')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'pais', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )


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

