from django.contrib import admin
from .models import Profile, Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["author", "content","post"]

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "bio", "avatar"]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)