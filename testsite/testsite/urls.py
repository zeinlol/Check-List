from django.contrib import admin
from django.urls import path, include
from  django.conf.urls import url
from checklist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('checklist.urls'), name='home'),
]