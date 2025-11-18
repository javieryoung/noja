from django.urls import path
from .views import Homepage, new_detail, news_list


urlpatterns = [
    path('', Homepage.as_view(), name='Homepage'),
    path('new/<int:pk>/', new_detail, name='new_detail'),
    path('news/', news_list, name='news_list'),



]
