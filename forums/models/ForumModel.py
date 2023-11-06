from django.db import models
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


class Forum(models.Model):
    ACCESSIBILITY_CHOICES = (
        ('open', _('Open')),
        ('subscribed', _('Subscribed'))
    )

    POSTING_PERMISSIONS_CHOICES = (
        ('creator_managers', _('Creators & Managers')),
        ('subscribers', _('Subscribers')),
        ('everyone', _('Everyone')),
    )

    id = models.UUIDField(
        _("Forum ID"),
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forums_created'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.URLField(blank=True, max_length=3000)
    description = models.TextField(max_length=1000, blank=True)
    accessibility = models.CharField(
        max_length=50,
        choices=ACCESSIBILITY_CHOICES,
        default='open'
    )
    posting_permissions = models.CharField(
        max_length=50,
        choices=POSTING_PERMISSIONS_CHOICES,
        default='everyone'
    )
    managers = models.ManyToManyField(
        User,
        blank=True,
        related_name='forums_managed'
    )
    subscribers = models.ManyToManyField(
        User,
        blank=True,
        related_name='subscribed_forums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Forum_detail", kwargs={"pk": self.pk})

    def can_user_post(self, user):
        if self.accessibility == 'subscribed':
            return user in self.subscribers.all()
        elif self.posting_permissions == 'everyone':
            return True
        elif self.posting_permissions == 'creator_managers':
            return user == self.author or user in self.managers.all()
        else:
            return False

    def save(self, *args, **kwargs):
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
    '''
    def total_threads(self):
        threads = Thread.objects.filter(forum=self).count()
        #threads = self.thread_set.count()
        return threads
        
    def total_posts(self):
        posts = Post.objects.filter(thread__forum=self).count()
        return posts
    
    def total_comments(self):
        comments = Comment.objects.filter(post__thread__forum=self).count()
        pass
    

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
        
    '''

    def total_threads(self):
        return Thread.objects.filter(forum=self).count()

    def total_posts(self):
        return Post.objects.filter(thread__forum=self).count()

    def total_comments(self):
        return Comment.objects.filter(post__thread__forum=self).count()

    def total_forum_upvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return UpVote.objects.filter(content_type=content_type, upvote_type='F').count()

    def total_forum_downvotes(self):
        content_type = ContentType.objects.get_for_model(self)
        return DownVote.objects.filter(content_type=content_type, upvote_type='F').count()

    def total_thread_upvotes(self):
        content_type = ContentType.objects.get_for_model(Thread)
        return UpVote.objects.filter(content_type=content_type, upvote_type='T',
                                     object_id__in=self.threads.values_list('id', flat=True)).count()

    def total_thread_downvotes(self):
        content_type = ContentType.objects.get_for_model(Thread)
        return DownVote.objects.filter(content_type=content_type, upvote_type='T',
                                       object_id__in=self.threads.values_list('id', flat=True)).count()

    def total_post_upvotes(self):
        content_type = ContentType.objects.get_for_model(Post)
        return UpVote.objects.filter(content_type=content_type, upvote_type='P',
                                     object_id__in=self.threads.values_list('posts__id', flat=True)).count()

    def total_post_downvotes(self):
        content_type = ContentType.objects.get_for_model(Post)
        return DownVote.objects.filter(content_type=content_type, upvote_type='P',
                                       object_id__in=self.threads.values_list('posts__id', flat=True)).count()

    def total_comment_upvotes(self):
        content_type = ContentType.objects.get_for_model(Comment)
        return UpVote.objects.filter(content_type=content_type, upvote_type='C',
                                     object_id__in=self.threads.values_list('posts__comments__id', flat=True)).count()

    def total_comment_downvotes(self):
        content_type = ContentType.objects.get_for_model(Comment)
        return DownVote.objects.filter(content_type=content_type, upvote_type='C',
                                       object_id__in=self.threads.values_list('posts__comments__id', flat=True)).count()

    def total_engagement(self):
        forum_upvotes = self.total_forum_upvotes()
        forum_downvotes = self.total_forum_downvotes()
        thread_upvotes = self.total_thread_upvotes()
        thread_downvotes = self.total_thread_downvotes()
        post_upvotes = self.total_post_upvotes()
        post_downvotes = self.total_post_downvotes()
        comment_upvotes = self.total_comment_upvotes()
        comment_downvotes = self.total_comment_downvotes()

        return (
                forum_upvotes + forum_downvotes +
                thread_upvotes + thread_downvotes +
                post_upvotes + post_downvotes +
                comment_upvotes + comment_downvotes
        )


class ForumRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ['author', 'forum']

    def __str__(self):
        return f'{self.author.get_username} rated {self.forum.title} with {self.rating} stars'
