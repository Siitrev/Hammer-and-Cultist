from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.utils.text import slugify 
from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import Post, Tag, TagsToPost, PostLikes
from .forms import CreatePostForm, CreateCommentForm, UpdatePostForm
from user.models import Comment
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.db import IntegrityError
from .handle_file import save_file
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from mysite.settings import GLOBAL_CONSTANTS
import json, datetime, os
import time, math, urllib
# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-likes")[:3]
    template_name = "blog/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        queryset = self.get_queryset()
        context = self.get_context_data(object_list=queryset)

        page_number = 1
        if "number" in kwargs:
            page_number = kwargs.get("number")

        tags = Tag.objects.all().values().order_by("name")
        context.update({"tag_list": tags})

        post_list = Post.objects.filter(status=1)

        req = request.GET
        if len(req):
            if "filter" in req:
                filters: list = req.getlist("filter")[:3]
                for tag in filters:
                    if tag != "":
                        post_list = post_list.filter(tag__id=tag)

            if "search" in req:
                if req["search"] or req["search"] != "":
                    search = urllib.parse.unquote(req["search"])
                    post_list = post_list.filter(title__contains=search)

            order = ""
            if req["order"] == "desc":
                order = "-"

            match req["sort"]:
                case "date":
                    post_list = post_list.order_by(f"{order}created_on")
                case "author":
                    if order == "-":
                        post_list = post_list.order_by(
                            Lower("author_id__username")
                        ).reverse()
                    else:
                        post_list = post_list.order_by(Lower("author_id__username"))
                case "title":
                    post_list = post_list.order_by(f"{order}slug")

        num_of_pages = math.ceil(len(post_list) / 6)

        context.update(
            {
                "search_post_list": post_list[(page_number - 1) * 6 : page_number * 6],
                "next_page": page_number + 1,
                "previous_page": page_number - 1,
                "active_page": page_number,
                "last_page": num_of_pages,
            }
        )

        if "no-refresh" in req:
            return render(request, "blog/all_posts.html", context=context)
        return render(request, self.template_name, context=context)


class PostDetail(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        post_id = context["post"].id
        context["comments_len"] = len(Comment.objects.filter(post_id=post_id))
        context["liked"] = False
        return context

    def get(self, request: HttpRequest, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user: User = request.user
        post: Post = context.get("post")
        if PostLikes.objects.filter(post_id=post.pk, user_id=user.pk):
            context["liked"] = True
            
        if user.is_authenticated:
            context["comment_form"] = CreateCommentForm(request.GET) 

        return render(request, self.template_name, context=context)
    
    def post(self, request: HttpRequest, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user: User = request.user
        post: Post = context.get("post")
        if PostLikes.objects.filter(post_id=post.pk, user_id=user.pk):
            context["liked"] = True
        
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data.get("content")
            
            if not comment:
                form.add_error("content","Comment can't be empty.")
                context["comment_form"] = form
                return render(request, self.template_name, context=context)
            
            Comment.objects.create(
                content = comment,
                author_id = user.pk,
                post_id = post.pk
            )
        
        context["comment_form"] = CreateCommentForm() 
        return redirect("post-detail", slug=post.slug)

    def put(self, request: HttpRequest, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        post: Post = context.get("post")
        try:
            if not request.user.is_authenticated:
                raise User.DoesNotExist
            post.likes += 1
            PostLikes.objects.create(post_id=post, user_id=request.user)
            post.save()
        except User.DoesNotExist as e:
            return HttpResponse(f"Forbidden", status=403)
        return HttpResponse(f"{post.likes}", status=200)

    def delete(self, request: HttpRequest, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        post: Post = context.get("post")
        try:
            if not request.user.is_authenticated:
                raise User.DoesNotExist
            post.likes -= 1
            PostLikes.objects.filter(post_id=post, user_id=request.user).delete()
            post.save()
        except User.DoesNotExist as e:
            return HttpResponse(f"Forbidden", status=403)
        return HttpResponse(f"{post.likes}", status=200)


def post_comments(request: HttpRequest, post_id):
    if request.method == "GET":
        maxCom = int(request.GET.get("maxCom"))
        comments = Comment.objects.filter(post_id=post_id).order_by("created_on")
        if maxCom - 1 >= len(comments):
            maxCom = len(comments)
        context = {
            "comments": Comment.objects.filter(post_id=post_id).order_by("-created_on")[
                :maxCom
            ]
        }
        return render(request, "blog/post_comments.html", context=context)
    return HttpResponse("Error. No get request", status=405)


def index(request: HttpRequest):
    return redirect("home")


@login_required(login_url="/user/login/")
def create_post(request: HttpRequest, username: str):
    try:
        user = User.objects.filter(username=username, pk=request.user.pk).get()
    except User.DoesNotExist:
        return HttpResponse("Forbidden resource", status=403)

    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return render(
                request=request,
                template_name="blog/post_configuration.html",
                context={"type" : "Create", "post_configuration_form": form},
            )
        
        img = form.files.get("image", None)
       
        try:
            img_path = GLOBAL_CONSTANTS["DEFAULT_THUMBNAIL_PATH"]
            if img:
                img_path = save_file(img, slugify(form.cleaned_data.get("title")))
        except ValidationError as e:
            form.add_error("image", e)
            return render(
                request=request,
                template_name="blog/post_configuration.html",
                context={"type" : "Create", "post_configuration_form": form},
            )

        user = User.objects.filter(username=username).get()

        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        draft = form.data.get("draft")
        
        status = 2
        if draft:
            status = 0

        today = datetime.datetime.now()

        try:
            created_post = Post.objects.create(
                title=title,
                content=content,
                author=user,
                updated_on=today,
                status=status,
                image=img_path,
                created_on=today,
            )
        except IntegrityError as e:
            form.add_error("title", "Post with given title already exists.")
            return render(
                request=request,
                template_name="blog/post_configuration.html",
                context={"type" : "Create", "post_configuration_form": form},
            )

        for index in range(3):
            tag_id = form.cleaned_data.get(f"chosen_tag_{index}")
            if tag_id is not None and tag_id != "":
                tag = Tag.objects.filter(id=tag_id).get()
                TagsToPost.objects.create(post=created_post, tag=tag)

        return redirect("user-posts", username)
    
    form = CreatePostForm()
    return render(
        request=request,
        template_name="blog/post_configuration.html",
        context={"type" : "Create", "post_configuration_form": form},
    )


@login_required(login_url="/user/login/")
def edit_post(request: HttpRequest, username: str, pk: int):
    try:
        user = User.objects.filter(username=username, pk=request.user.pk).get()
    except User.DoesNotExist:
        return HttpResponse("Forbidden resource", status=403)
    
    user_post = Post.objects.filter(pk=pk).get()
    
    if request.method == "GET":
        post_tags = TagsToPost.objects.filter(post = user_post)
        
        tags = ["", "", ""]
        
        for i in range(post_tags.count()):
            tags[i] = str(post_tags[i].tag.pk)
        
        form = UpdatePostForm(initial={
            "title" : user_post.title,
            "content": user_post.content,
            "image" : user_post.image,
            "chosen_tag_0" : tags[0],
            "chosen_tag_1" : tags[1],
            "chosen_tag_2" : tags[2],
            "submit": "Update",
        })
    
        return render(request=request, template_name="blog/post_configuration.html", context={"type" : "Update", "post_configuration_form": form})
    
    if request.method == "POST":
        form = UpdatePostForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return render(
                request=request,
                template_name="blog/post_configuration.html",
                context={"type" : "Create", "post_configuration_form": form},
            )
        
        img = form.files.get("image", None)
        new_slug = slugify(form.cleaned_data.get("title"))        
        try:
            if img:
                img_path = save_file(img, new_slug) 
            elif new_slug != user_post.slug:
                img_path = save_file(user_post.image.file, new_slug, True)
        except ValidationError as e:
            form.add_error("image", e)
            return render(
                request=request,
                template_name="blog/post_configuration.html",
                context={"type" : "Update", "post_configuration_form": form},
            )
    
        TagsToPost.objects.filter(post = user_post).delete()
        
        for index in range(3):
            tag_id = form.cleaned_data.get(f"chosen_tag_{index}")
            if tag_id is not None and tag_id != "":
                tag = Tag.objects.filter(id=tag_id).get()
                TagsToPost.objects.create(post=user_post, tag=tag)
                
        user_post.title = form.cleaned_data.get("title")
        user_post.content = form.cleaned_data.get("content")
        
        if img != user_post.image and (img or new_slug != user_post.slug):
            user_post.image = img_path
        
        user_post.save()
                
        return redirect("user-posts", username)
        
        

@login_required(login_url="/user/login/")
def delete_post(request: HttpRequest, username: str, pk: int):
    try:
        user = User.objects.filter(username=username, pk=request.user.pk).get()
    except User.DoesNotExist:
        return HttpResponse("Forbidden resource", status=403)

    if request.method == "DELETE":
        Post.objects.filter(id=pk).delete()
        return HttpResponse("Success", status=200)
    

@login_required(login_url="/user/login/")
def publish_post(request: HttpRequest, username: str, pk: int):
    try:
        user = User.objects.filter(username=username, pk=request.user.pk).get()
    except User.DoesNotExist:
        return HttpResponse("Forbidden resource", status=403)

    if request.method == "PATCH":
        post = Post.objects.filter(pk=pk).get()
        post.status = 2
        post.save()
        url = reverse("user-posts", args=[username])
        
        return HttpResponseRedirect(url, status=303)
        
        
