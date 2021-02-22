from django.conf.urls import url, include
from . import views
from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView
from checklist.models import CheckList


urlpatterns = [
    url(r'^$', views.show_lists, name='home'),
    path('uncross_list/<list_id>', views.uncross_list, name='uncross_list'),
    path('cross_list/<list_id>', views.cross_list, name='cross_list'),
    path('uncross_category/<category_id>', views.uncross_category, name='uncross_category'),
    path('cross_category/<category_id>', views.cross_category, name='cross_category'),
    path('uncross_subtask/<item_id>', views.uncross_subtask, name='uncross_subtask'),
    path('cross_subtask/<item_id>', views.cross_subtask, name='cross_subtask'),
    path('checklist/<list_id>', views.show_full_list, name='checklist'),
    path('editlist/<list_id>', views.edit_list, name='editlist'),
]
