from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from forums.models.ForumModel import *
from forums.models.CommentModel import Comment

User = get_user_model()



class Reply(DateTimeModel):

    author = ForeignKey(User, on_delete=CASCADE, related_name="upvotes")
    comment = ForeignKey(Comment, on_delete=CASCADE)
    content = TextField(max_length=1000)

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replys")

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse("Reply_detail", kwargs={"pk": self.pk})


VOTE_TYPES = (
        ('T', 'Thread'),
        ('P', 'Comment'),
        ('C', 'Comment'),
        ('R', 'Reply'),
    )

class UpVote(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    upvote_type = CharField(max_length=1, choices=VOTE_TYPES)
    
    class Meta:
        verbose_name = _("Upvote")
        verbose_name_plural = _("Upvotes")

    def get_upvote_type(self):
        return dict(VOTE_TYPES)[self.upvote_type]


class DownVote(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    upvote_type = CharField(max_length=1, choices=VOTE_TYPES)

    class Meta:
        verbose_name = _("Downvote")
        verbose_name_plural = _("Downvotes")

    def get_upvote_type(self):
        return dict(VOTE_TYPES)[self.upvote_type]



