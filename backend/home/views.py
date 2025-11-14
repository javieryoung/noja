from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm
from django.views import View
from .constants import COUNTRIES_KEYS
from .models import New
from django.core.paginator import Paginator
from django.http import JsonResponse



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

def news_list(request):
    news_queryset = New.objects.all().order_by('-date')
    paginator = Paginator(news_queryset, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        news_data = [
            {'id': n.id, 'title': n.title}
            for n in page_obj
        ]
        return JsonResponse({
            'news': news_data,
            'page': page_obj.number,
            'total_pages': paginator.num_pages,
        })

    return render(request, 'news.html', {'news': page_obj})

