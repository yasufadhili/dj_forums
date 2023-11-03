from django.contrib import admin
from forums.models.PostModel import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #list_display = ('content', 'thread__forum__title', 'author', 'created_at', 'views')
    list_display = ('content', 'thread', 'author', 'created_at', 'views')
    list_filter = ('thread', 'thread__forum')
    search_fields = ('content', 'thread__title' 'thread__forum__title', 'author__username')
