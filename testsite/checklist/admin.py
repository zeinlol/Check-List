from django.contrib import admin
from checklist.models import CheckList, Category, SubTask, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(CheckList)
admin.site.register(Category)
admin.site.register(SubTask)
admin.site.register(Comment, CommentAdmin)

