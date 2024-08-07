from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from mysite.settings import GLOBAL_CONSTANTS
import os
from .models import Post


@receiver(post_delete, sender=Post)
def delete_thumbnail(sender, instance : Post, **kwargs):
    global_path = os.path.normpath(GLOBAL_CONSTANTS["DEFAULT_THUMBNAIL_PATH"])
    old_path = os.path.normpath(instance.image.path)
    
    
    if global_path in old_path:
        return False
    
    if os.path.exists(old_path):
        os.remove(old_path)
                
    parent_directory = os.path.dirname(old_path)                
                    
    if os.path.exists(parent_directory) and not os.listdir(parent_directory):
        os.rmdir(parent_directory)
    
    day_directory = os.path.dirname(parent_directory)    
        
    if os.path.exists(day_directory) and not os.listdir(day_directory):
        os.rmdir(day_directory)
        
@receiver(pre_save, sender=Post)
def remove_old_file_and_path(sender, instance : Post, **kwargs):
    try:
        old_file = Post.objects.filter(pk = instance.pk).get()
    except Post.DoesNotExist:
        return False
    
    global_path = os.path.normpath(GLOBAL_CONSTANTS["DEFAULT_THUMBNAIL_PATH"])
    old_path = os.path.normpath(old_file.image.path)
    new_path = os.path.normpath(instance.image.path)
    
    if global_path in old_path:
        return False
    
    if old_path == new_path:
        return False
    
    if os.path.exists(old_path):
        os.remove(old_path)
        
    parent_directory = os.path.dirname(old_path)    
        
    if os.path.exists(parent_directory) and not os.listdir(parent_directory):
        os.rmdir(parent_directory)
    
    