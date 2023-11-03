from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *


User = get_user_model()


class Thread(DateFields):

    forum = ForeignKey(Forum, verbose_name=_("Thread Forum"), on_delete=CASCADE)
    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    content = TextField(max_length=1000)

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Thread_detail", kwargs={"pk": self.pk})


