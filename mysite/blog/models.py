from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
from mysite.settings import GLOBAL_CONSTANTS

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish"),
    (2,"Waiting for approval"),
    (3,"Watitng for deletion")
)

class TitleCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        super(TitleCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.title()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(TitleCharField, self).pre_save(model_instance, add)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/featured_image/%Y/%m/%d/', default=GLOBAL_CONSTANTS["DEFAULT_THUMBNAIL_PATH"])
    content = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
        ordering = ['-created_on']
    
    def __str__(self) -> str:
        return self.title    
  
class Tag(models.Model):

    name = TitleCharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    posts = models.ManyToManyField(Post, through="TagsToPost", through_fields=("tag","post"))

    class Meta:
        verbose_name = ("Tag")
        verbose_name_plural = ("Tags")

    def __str__(self):
        return self.name  
    
class TagsToPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.post} {self.tag}" 
    
 
class PostLikes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)



