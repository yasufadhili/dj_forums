from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType

from forums.models.EngagementModel import DownVote, UpVote
from forums.models.PostModel import Post

User = get_user_model()

class Thread(models.Model):
    id = models.UUIDField(
        _("Thread ID"),
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    forum = models.ForeignKey(
        'forums.Forum',
        on_delete=models.CASCADE,
        related_name='threads'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(max_length=1000, blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('thread_detail', args=[str(self.pk), self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)

    def total_posts(self):
        posts = Post.objects.filter(thread=self).count()
        return posts

    def increment_views(self):
        self.views += 1
        self.save()

    def total_thread_upvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return UpVote.objects.filter(content_type=content_type, upvote_type='T', object_id=self.id).count()

    def total_thread_downvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return DownVote.objects.filter(content_type=content_type, upvote_type='T', object_id=self.id).count()
