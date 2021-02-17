from django.contrib import admin
from django.urls import path, include
from  django.conf.urls import url
from django.views.generic import ListView, DetailView, TemplateView
from checklist.models import CheckList

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('checklist.urls'), name='home'),
]