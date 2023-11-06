from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upvotes")
    comment = models.ForeignKey('forums.Comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse("Reply_detail", kwargs={"pk": self.pk})


class UpVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    VOTE_TYPES = (
        ('T', 'Thread'),
        ('P', 'Post'),
        ('C', 'Comment'),
        ('R', 'Reply'),
    )

    upvote_type = models.CharField(max_length=1, choices=VOTE_TYPES)

    class Meta:
        verbose_name = _("Upvote")
        verbose_name_plural = _("Upvotes")

    def get_upvote_type(self):
        return dict(self.VOTE_TYPES)[self.upvote_type]


class DownVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    upvote_type = models.CharField(max_length=1, choices=UpVote.VOTE_TYPES)

    class Meta:
        verbose_name = _("Downvote")
        verbose_name_plural = _("Downvotes")

    def get_upvote_type(self):
        return dict(UpVote.VOTE_TYPES)[self.upvote_type]


# Utility function to get total upvotes and downvotes for a given model
def get_total_upvotes(model, object_id, upvote_type):
    content_type = ContentType.objects.get_for_model(model)
    return UpVote.objects.filter(content_type=content_type, object_id=object_id, upvote_type=upvote_type).count()


def get_total_downvotes(model, object_id, upvote_type):
    content_type = ContentType.objects.get_for_model(model)
    return DownVote.objects.filter(content_type=content_type, object_id=object_id, upvote_type=upvote_type).count()
