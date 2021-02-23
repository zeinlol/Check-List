from django.contrib import admin
from checklist.models import CheckList, Category, SubTask, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_list')
    list_filter = ('completed', 'related_list')
    search_fields = ('title',)


class SubtasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_category')
    list_filter = ('completed', 'related_category')
    search_fields = ('title',)


class ListsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'completed')
    list_filter = ('name', 'date', 'completed')
    search_fields = ('name',)


admin.site.register(CheckList, ListsAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(SubTask, SubtasksAdmin)
admin.site.register(Comment, CommentAdmin)

