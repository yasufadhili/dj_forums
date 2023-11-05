from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from forums.models.ForumModel import *
from forums.models.CommentModel import Comment

User = get_user_model()



class Reply(Model):

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
    
    def total_upvotes(self):
        return get_total_upvotes(self, self.id, 'R')

    def total_downvotes(self):
        return get_total_downvotes(self, self.id, 'R')


VOTE_TYPES = (
        ('T', 'Thread'),
        ('P', 'Post'),
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


# utility function to get total upvotes and downvotes for a given model
def get_total_upvotes(model, object_id, upvote_type):
    content_type = ContentType.objects.get_for_model(model)
    return UpVote.objects.filter(content_type=content_type, object_id=object_id, upvote_type=upvote_type).count()

def get_total_downvotes(model, object_id, upvote_type):
    content_type = ContentType.objects.get_for_model(model)
    return DownVote.objects.filter(content_type=content_type, object_id=object_id, upvote_type=upvote_type).count()


