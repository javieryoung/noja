from django.views import View
from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm, NewAdminForm
from .constants import COUNTRIES_KEYS
from .models import New



class Homepage(View):
    def get(self, request):
        form = CustomUserCreationForm()
        news = New.objects.order_by('-date')
        return render(request, 'home-content.html', context={
            'form': form,
            'countries': COUNTRIES_KEYS,
            'news_list': news
        })

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        news = New.objects.order_by('-date')
        if form.is_valid():
            form.save()
            return render(request, 'home-content.html', context={
                'form': CustomUserCreationForm(),  # formulario limpio
                'success_message': 'Formulario guardado correctamente',
                'countries': COUNTRIES_KEYS,
                'news_list': news
            })
        else:
            return render(request, 'home-content.html', context={
                'form': form,
                'countries': COUNTRIES_KEYS
            })
    
def new_detail(request, pk):
    new = get_object_or_404(New, pk=pk)
    return render(request, 'new_detail.html', {'new': new})



