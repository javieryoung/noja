
import os
from django.contrib import admin
from django.urls import path, include
from noja import settings
from django.conf.urls.static import static

handler404 = "home.views.custom_page_not_found"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('tinymce/', include('tinymce.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


