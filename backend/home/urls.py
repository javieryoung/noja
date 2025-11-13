from django.urls import path
from .views import Homepage, new_detail


urlpatterns = [
    path('homepage/', Homepage.as_view(), name='Homepage'),
    path('noticia/<int:pk>/', new_detail, name='new_detail'),


]
