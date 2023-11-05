from django.db.models import (
    Model, CharField,
    TextField,
    SlugField,
    DateTimeField,
    URLField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
    PositiveIntegerField,
    UUIDField,
    
)
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid

from forums.models.ThreadModel import Thread
from forums.models.PostModel import Post
from forums.models.CommentModel import Comment
from forums.models.EngagementModel import UpVote, DownVote, get_total_upvotes, get_total_downvotes


User = get_user_model()


class Forum(Model):

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

    id = UUIDField(_("Forum ID"),
                   primary_key=True,
                   unique=True,
                   editable=False,
                   default=uuid.uuid4)
    author = ForeignKey(User, on_delete=CASCADE, related_name='forums_created')
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    image = URLField(blank=True, max_length=3000)
    description = TextField(max_length=1000, blank=True)
    accessibility = CharField(max_length=50, choices=ACCESSIBILITY_CHOICES, default='open')
    posting_permissions = CharField(max_length=50, choices=POSTING_PERMISSIONS_CHOICES, default='everyone')
    managers = ManyToManyField(User, blank=True, related_name='forums_managed')
    subscribers = ManyToManyField(User, blank=True, related_name='subscribed_forums')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("Forum_detail", kwargs={"pk": self.pk})
    
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
            return user == self.author or user in self.managers.all()
        else:
            return False  # Default to not allowing the user to post
    
    def save(self, *args, **kwargs):
        # Generate a unique slug based on title and user's pk
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            user_pk = str(self.author.pk)
            counter = 1

            while Forum.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{user_pk}-{counter}"
                counter += 1

            self.slug = unique_slug

        super(Forum, self).save(*args, **kwargs)
    
    def total_threads(self):
        threads = Thread.objects.filter(forum=self).count()
        #threads = self.thread_set.count()
        return threads

    '''
    def total_posts(self):
        posts = Post.objects.filter(thread__forum=self).count()
        return posts
    
    def total_comments(self):
        comments = Comment.objects.filter(post__thread__forum=self).count()
        pass
    '''

    def total_thread_upvotes(self):
        upvotes = UpVote.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                        upvote_type='T').count()
        return upvotes
    
    def total_thread_downvotes(self):
        downvotes = DownVote.objects.filter(content_type=ContentType.objects.get_for_model(self),
                                            upvote_type='T').count()
        return downvotes

    def total_engagement(self):
        pass

class ForumRating(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    forum = ForeignKey(Forum, on_delete=CASCADE)
    rating = PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ['author', 'forum']  # Ensure a user can rate a forum only once

    def __str__(self):
        return f'{self.author.get_username} rated {self.forum.title} with {self.rating} stars'


