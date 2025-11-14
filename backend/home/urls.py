from django.urls import path
from .views import Homepage


urlpatterns = [
    path('homepage/', Homepage.as_view(), name='Homepage'),
]
