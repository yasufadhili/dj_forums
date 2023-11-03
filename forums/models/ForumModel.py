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


class DateFields(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Forum(DateFields):

    ACCESSIBILITY_CHOICES = (
        ('open', 'Open'),
        ('subscribed', 'Subscribed')
    )

    POSTING_PERMISSIONS_CHOICES = (
        #('creator', 'Creator'),
        ('creator_managers', 'Creators & Managers'),
        ('subscribers', 'Subscribers'),
        ('everyone', 'Everyone'),
    )

    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    image = URLField(blank=True, max_length=3000)
    description = TextField(max_length=1000, blank=True)
    managers  = ManyToManyField(User, verbose_name=_("Forum managers"))
    accessibility = CharField(max_length=50, choices=ACCESSIBILITY_CHOICES, default='open')
    posting_permissions = CharField(max_length=50, choices=POSTING_PERMISSIONS_CHOICES, default='everyone')
    subscribers = ManyToManyField(User, related_name='subscribed_forums', default='creator_managers', blank=True)

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("Forum_detail", kwargs={"pk": self.pk})
    
    def can_user_post(self, user):
        if self.accessibility == "subscribed":
            return user in self.subscribers.all()
        elif self.posting_permissions == 'everyone':
            return True
        else:
            return False
        
    def can_user_post(self, user):
        if self.accessibility == 'subscribed':
            # If the forum is 'subscribed', check if the user is a subscriber
            return user in self.subscribers.all()
        elif self.posting_permissions == 'everyone':
            # If the posting permissions are set to 'everyone', anyone can post
            return True
        elif self.posting_permissions == 'creator_managers':
            # If the posting permissions are set to 'creator & managers',
            # check if the user is the creator or a designated manager
            return user == self.author or user in self.managers .all()
        else:
            return False  # Default to not allowing the user to post



