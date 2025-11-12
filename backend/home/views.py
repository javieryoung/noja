from django.views import View
from django.shortcuts import render
from .forms import CustomUserCreationForm
from .constants import COUNTRIES_KEYS


class Homepage(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'home-content.html', context={
            'form': form,
            'countries': COUNTRIES_KEYS
        })

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home-content.html', context={
                'form': CustomUserCreationForm(),  # formulario limpio
                'success_message': 'Formulario guardado correctamente',
                'countries': COUNTRIES_KEYS
            })
        else:
            return render(request, 'home-content.html', context={
                'form': form,
                'countries': COUNTRIES_KEYS
            })

