from django.conf.urls import url, include
from . import views
from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView
from checklist.models import CheckList


urlpatterns = [
    url(r'^$', views.show_list),
    path('cross_item/<list_id>', views.cross_item, name='cross_off'),
    path('uncross_item/<list_id>', views.uncross_item, name='uncross'),

]
