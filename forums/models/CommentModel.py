from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from forums.models.EngagementModel import DownVote, UpVote

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey('forums.Post', on_delete=models.CASCADE, related_name="thread_post_comments")
    content = models.TextField(max_length=1000)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def total_comment_upvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return UpVote.objects.filter(content_type=content_type, upvote_type='C', object_id=self.id).count()

    def total_comment_downvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return DownVote.objects.filter(content_type=content_type, upvote_type='C', object_id=self.id).count()
