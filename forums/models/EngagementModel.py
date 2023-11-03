from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *
from forums.models.CommentModel import Comment

User = get_user_model()



class Reply(Model):

    author = ForeignKey(User, on_delete=CASCADE, related_name="upvotes")
    comment = ForeignKey(Comment, on_delete=CASCADE)
    content = TextField(max_length=1000)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replys")

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse("Reply_detail", kwargs={"pk": self.pk})



class Upvote(Model):

    author = ForeignKey(User, on_delete=CASCADE, related_name="upvotes")
    comment = ForeignKey(Comment, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Upvote")
        verbose_name_plural = _("Upvotes")

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse("Upvote_detail", kwargs={"pk": self.pk})


class Downvote(Model):

    author = ForeignKey(User, on_delete=CASCADE, related_name="downvotes")

    class Meta:
        verbose_name = _("Downvote")
        verbose_name_plural = _("Downvotes")

    def __str__(self):
        return self.author

    def get_absolute_url(self):
        return reverse("Downvote_detail", kwargs={"pk": self.pk})



