from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from mysite.settings import GLOBAL_CONSTANTS
import os
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(pre_save, sender=Profile)
def delete_old_file(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    file = instance.avatar
    if not old_file == file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            


@receiver(pre_save, sender=User)
def remove_old_file_and_path(sender, instance : User, **kwargs):
    try:
        old_user = User.objects.filter(pk = instance.pk).get()
    except User.DoesNotExist:
        return False
    
    global_path = os.path.normpath(GLOBAL_CONSTANTS["DEFAULT_AVATAR_PATH"])
    old_path = os.path.normpath(old_user.profile.avatar.path)
    new_path = os.path.normpath(instance.profile.avatar.path)
    
    if global_path in old_path:
        return False
    
    if old_path == new_path:
        return False
    
    if os.path.exists(old_path):
        os.remove(old_path)
        
    parent_directory = os.path.dirname(old_path)    
        
    if os.path.exists(parent_directory) and not os.listdir(parent_directory):
        os.rmdir(parent_directory)