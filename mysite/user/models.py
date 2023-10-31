from django.db import models
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

def img_path(instance, filename):
    ext = filename[-4:]
    filename = urlsafe_base64_encode(force_bytes(filename[:-4]))
    return f"media/profile_image/{instance.user.username}/{filename}{ext}"

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=600,default="")
    avatar = models.ImageField(upload_to=img_path, default="static/images/default-profile-picture.jpg")
    
    def __str__(self):
        return self.user.username
    
