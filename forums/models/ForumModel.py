from django.db.models import (
    Model, CharField,
    TextField,
    SlugField,
    DateTimeField,
    URLField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
)
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Forum(Model):

    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    image = URLField(blank=True, max_length=3000)
    description = TextField(max_length=1000, blank=True)
    moderators = ManyToManyField(User, verbose_name=_("Forum moderators"))
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Forum_detail", kwargs={"pk": self.pk})


