from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
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