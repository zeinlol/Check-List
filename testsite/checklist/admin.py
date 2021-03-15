from django.contrib import admin

from .models import CheckList, Comment, ListItem, Status


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


class ListItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_list', 'date')
    list_filter = ('done', 'related_list', 'date')
    search_fields = ('title', 'related_list',)


class ListsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'done')
    list_filter = ('name', 'date', 'done')
    search_fields = ('name',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('id',)
    search_fields = ('title',)


admin.site.register(CheckList, ListsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ListItem, ListItemsAdmin)
admin.site.register(Status, StatusAdmin)
