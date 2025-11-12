
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from noja import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('tinymce/', include('tinymce.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


