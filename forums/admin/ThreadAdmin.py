from django.contrib import admin
from forums.models.ThreadModel import Thread

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'created_at', 'views')
    list_filter = ('forum',)
    search_fields = ('title', 'forum__title', 'author__username')
