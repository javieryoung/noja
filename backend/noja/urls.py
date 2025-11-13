
import os
from django.contrib import admin
from django.urls import path, include
from noja import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('tinymce/', include('tinymce.urls')),


]
