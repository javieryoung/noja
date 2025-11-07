from django.http import JsonResponse, HttpResponseBadRequest
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok', 'message': 'Usuario creado correctamente'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return HttpResponseBadRequest("Solo se acepta POST.")