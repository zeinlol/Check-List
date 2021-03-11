from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'lists', views.CheckListViewSet)
router.register(r'items', views.ListItemViewSet)

urlpatterns = router.urls

# # # # # # # # # # # # # # # #  OLD URLS
#     urlpatterns = [
#     url(r'^$', views.show_lists, name='home')
#     path('uncross_list/<list_id>', views.uncross_list, name='uncross_list'),
#     path('cross_list/<list_id>', views.cross_list, name='cross_list'),
#     path('uncross_item/<item_id>', views.uncross_item, name='uncross_item'),
#     path('cross_item/<item_id>', views.cross_item, name='cross_item'),
#     path('checklist/<list_id>', views.show_full_list, name='checklist'),
#     path('editlist/<list_id>', views.edit_list, name='editlist'),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     ]
