from django.contrib import admin
from forums.models.ForumModel import Forum
from forums.models.ThreadModel import Thread
from forums.models.PostModel import Post
from forums.models.CommentModel import Comment
from forums.models.EngagementModel import UpVote, DownVote


class ThreadInline(admin.TabularInline):
    model = Thread
    extra = 0


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ForumAdmin(admin.ModelAdmin):
    inlines = [ThreadInline]
    list_display = (
    'title', 'total_threads', 'total_posts', 'total_comments', 'total_forum_upvotes', 'total_forum_downvotes',
    'total_engagement')

    def total_threads(self, obj):
        return obj.total_threads()

    def total_posts(self, obj):
        return obj.total_posts()

    def total_comments(self, obj):
        return obj.total_comments()

    def total_forum_upvotes(self, obj):
        return obj.total_forum_upvotes()

    def total_forum_downvotes(self, obj):
        return obj.total_forum_downvotes()

    def total_engagement(self, obj):
        return obj.total_engagement()


class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('title', 'forum', 'total_posts', 'total_thread_upvotes', 'total_thread_downvotes')


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('sliced_content', 'thread', 'total_comments', 'total_post_upvotes', 'total_post_downvotes')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'total_comment_upvotes', 'total_comment_downvotes')


class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'content_type', 'object_id', 'upvote_type')


class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'content_type', 'object_id', 'upvote_type')


admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UpVote, UpVoteAdmin)
admin.site.register(DownVote, DownVoteAdmin)
