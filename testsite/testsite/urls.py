from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url('', include('checklist.urls'), name='home'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
