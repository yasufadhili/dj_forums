from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *
from forums.models.PostModel import Post

User = get_user_model()


class Comment(Model):

    post = ForeignKey(Post, on_delete=CASCADE, related_name="thread_post_comments")
    content = TextField(max_length=1000)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    dislikes = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})

    '''
    def total_upvotes(self):
        return get_total_upvotes(self, self.id, 'C')

    def total_downvotes(self):
        return get_total_downvotes(self, self.id, 'C')
    '''
    
    def increment_views(self):
        self.views += 1
        self.save()

    def total_comment_upvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return UpVote.objects.filter(content_type=content_type, upvote_type='C', object_id=self.id).count()

    def total_comment_downvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return DownVote.objects.filter(content_type=content_type, upvote_type='C', object_id=self.id).count()


