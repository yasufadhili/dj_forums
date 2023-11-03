from django.db.models.signals import post_save
from django.dispatch import receiver
from forums.models.ForumModel import Forum

@receiver(post_save, sender=Forum)
def add_creator_to_managers(sender, instance, created, **kwargs):
    if created:
        # If a new forum is created, add the creator to the managers
        instance.managers.add(instance.author)
