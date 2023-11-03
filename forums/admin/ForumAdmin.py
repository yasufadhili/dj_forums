from django.contrib import admin
from forums.models.ForumModel import Forum

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'accessibility', 'posting_permissions')
    list_filter = ('accessibility', 'posting_permissions')
    search_fields = ('title', 'author__username')

