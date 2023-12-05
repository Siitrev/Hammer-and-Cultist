from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post-detail"),
    path("<int:post_id>/comments", views.post_comments, name="post-comments"),
]
