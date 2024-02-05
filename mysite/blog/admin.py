from django.contrib import admin
from .models import Post, Tag, TagsToPost
from .forms import TagsToPostForm

class PostAdmin(admin.ModelAdmin):
    list_display = ("title","slug","status","created_on")
    list_filter = ("status",)
    search_fields = ["title","content"]
    prepopulated_fields = {'slug': ("title",)}

class TagsToPostAdmin(admin.ModelAdmin):
    form = TagsToPostForm
    
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}
    
    
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagsToPost, TagsToPostAdmin)