from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from tinymce.widgets import TinyMCE
from .models import New



class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'nombre', 'pais', 'telefono']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
    
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


