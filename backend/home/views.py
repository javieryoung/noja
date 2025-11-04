from django.shortcuts import render

# Create your views here.


def home_view(request):
    datos = {
        'titulo_pagina': 'Info de Inicioq'

    }
    return render(request, 'index.html', datos)
