from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *


User = get_user_model()


class Thread(Model):

    forum = ForeignKey(Forum, on_delete=CASCADE, related_name='threads')
    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    content = TextField(max_length=1000)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Thread_detail", kwargs={"pk": self.pk})


