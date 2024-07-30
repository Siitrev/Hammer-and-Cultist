from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import Post


@receiver(post_delete, sender=Post)
def delete_thumbnail(sender, instance : Post, **kwargs):
    if os.path.exists(instance.image.path):
        os.remove(instance.image.path)
                
    parent_directory = os.path.dirname(instance.image.path)                
                
    if os.path.exists(parent_directory) and not os.listdir(parent_directory):
        os.rmdir(parent_directory)