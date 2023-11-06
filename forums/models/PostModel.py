from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.contenttypes.models import ContentType

from forums.models.CommentModel import Comment
from forums.models.EngagementModel import DownVote, UpVote

User = get_user_model()

class Post(models.Model):
    id = models.UUIDField(
        _("Post ID"),
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="thread_posts"
    )
    thread = models.ForeignKey('forums.Thread', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread Post")
        verbose_name_plural = _("Thread Posts")

    def __str__(self):
        return f"{self.content[:50]}"

    def get_absolute_url(self):
        return reverse("ThreadPost_detail", kwargs={"pk": self.pk})

    def sliced_content(self):
        return self.content[:40]

    def increment_views(self):
        self.views += 1
        self.save()

    def total_comments(self):
        return Comment.objects.filter(post__thread__post=self).count()

    def total_post_upvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return UpVote.objects.filter(content_type=content_type, upvote_type='P', object_id=self.id).count()

    def total_post_downvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return DownVote.objects.filter(content_type=content_type, upvote_type='P', object_id=self.id).count()
