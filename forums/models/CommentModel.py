from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *
from forums.models.PostModel import Post

User = get_user_model()


class Comment(DateTimeModel):

    post = ForeignKey(Post, on_delete=CASCADE, related_name="thread_post_comments")
    content = TextField(max_length=1000)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    dislikes = PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})
    
    def increment_views(self):
        self.views += 1
        self.save()

    def increment_likes(self):
        self.likes += 1
        self.save()

    def increment_dislikes(self):
        self.dislikes += 1
        self.save()


