from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from forums.models.ForumModel import *


User = get_user_model()


class Thread(Model):

    id = UUIDField(_("Forum ID"),
                   primary_key=True,
                   unique=True,
                   editable=False,
                   default=uuid.uuid4)
    forum = ForeignKey("Forum", on_delete=CASCADE, related_name='threads')
    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=255)
    slug = SlugField(unique=True, blank=True)
    content = TextField(max_length=1000, blank=True)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    dislikes = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('thread_detail', args=[str(self.pk), self.slug])
    
    def save(self, *args, **kwargs):
        # Generate a unique slug based on the title
        if not self.slug:
            self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)
    
    def total_posts(self):
        posts = Post.objects.filter(thread__forum=self).count()
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
    


