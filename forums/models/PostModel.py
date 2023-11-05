
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *
from forums.models.ThreadModel import Thread

User = get_user_model()


class Post(Model):

    id = UUIDField(_("Forum ID"),
                   primary_key=True,
                   unique=True,
                   editable=False,
                   default=uuid.uuid4)
    author = ForeignKey(User, on_delete=CASCADE, related_name="thread_posts")
    thread = ForeignKey(Thread, on_delete=CASCADE)
    content = TextField(max_length=1000)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    dislikes = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread Post")
        verbose_name_plural = _("Thread Posts")

    def __str__(self):
        return f"{self.content[:50]}"
    
    def get_absolute_url(self):
        return reverse("ThreadPost_detail", kwargs={"pk": self.pk})
    
    def total_upvotes(self):
        return get_total_upvotes(self, self.id, 'P')

    def total_downvotes(self):
        return get_total_downvotes(self, self.id, 'P')
    
    def increment_views(self):
        self.views += 1
        self.save()

    def increment_likes(self):
        self.likes += 1
        self.save()

    def increment_dislikes(self):
        self.dislikes += 1
        self.save()


