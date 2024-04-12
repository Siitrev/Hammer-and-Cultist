from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("page/<int:number>", views.PostList.as_view(), name="blog-page"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post-detail"),
    path("<int:post_id>/comments", views.post_comments, name="post-comments"),
    path("<str:username>/create-post", views.create_post, name="create-post"),
    path("<str:username>/edit-post/<int:pk>", views.edit_post, name="edit-post"),
    path("<str:username>/delete-post/<int:pk>", views.delete_post, name="delete-post"),
]
