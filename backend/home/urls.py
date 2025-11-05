from django.urls import path
from .views import layout


urlpatterns = [
    path('homepage/', layout),
]
