from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic
from django.http import HttpRequest, HttpResponse
from .models import Post, Tag, TagsToPost
from .forms import CreatePostForm
from user.models import Comment
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .handle_file import save_file
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json, datetime
# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-likes")
    template_name = "blog/index.html"
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        queryset = self.get_queryset()
        context = self.get_context_data(object_list=queryset)
        tags = Tag.objects.all().values().order_by("name")
        context.update({"tag_list" :tags})
        return render(request, self.template_name, context=context)
    
class PostDetail(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        post_id = context["post"].id
        context["comments_len"] = len(Comment.objects.filter(post_id=post_id))
        return context
    
    def get(self, request : HttpRequest, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context=context)
    
def post_comments(request : HttpRequest, post_id):
        if request.method == "GET":
            maxCom = int(request.GET.get("maxCom"))
            comments = Comment.objects.filter(post_id=post_id).order_by("created_on")
            if (maxCom-1 >= len(comments)):
                maxCom = len(comments)
            context = {"comments" : Comment.objects.filter(post_id=post_id).order_by("created_on")[:maxCom]};
            return render(request,"blog/post_comments.html", context=context)
        return HttpResponse("Error. No get request", status=405)
    

def search_posts(request : HttpRequest):
    if request.method == "GET":
        if len(request.GET) == 0:
            post_list = Post.objects.filter(status=1)
            return render(request,"blog/all_posts.html", context={"post_list":post_list})
        return HttpResponse("Too many get parameters.")
    
    if request.method == "POST":
        res : dict = json.loads(request.body)
        
        post_list = Post.objects.all()
        
        order = ""
        if res["order"] == "desc":
            order = "-"
        match res["sort"]:
            case "date":
                post_list = post_list.order_by(f"{order}created_on")
            case "author":
                if order == "-":
                    post_list = post_list.order_by(Lower("author_id__username")).reverse()
                else:
                    post_list = post_list.order_by(Lower("author_id__username"))
            case "title":
                post_list = post_list.order_by(f"{order}slug")
        
        filters : list = res["filters"]
        for tag in filters:
            post_list = post_list.filter(tag__id=tag)
            
        
        return render(request,"blog/all_posts.html", context={"post_list":post_list})
    return HttpResponse("Error. No get request")

def index(request : HttpRequest):
    return redirect("home")

@login_required(login_url="/user/login/")
def create_post(request : HttpRequest, username : str):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        
        if form.is_valid():
            img = form.files["image"]
            try:
                img_path = save_file(img)
            except ValidationError as e:
                form.add_error("image", e)
                return render(request=request, template_name="blog/create_post.html", context={"create_post_form" : form})
        
        
        user = User.objects.filter(username=username).get()
        
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")
        
        match form.data.get("submit"):
            case "Create":
                status = 2
            case "Draft":
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
                created_on=today
            )
        except IntegrityError as e:
            form.add_error("title", "Post with given title already exists.")
            return render(request=request, template_name="blog/create_post.html", context={"create_post_form" : form})
        
            
        for index in range(3):
            tag_id = form.cleaned_data.get(f"chosen_tag_{index}")
            if tag_id is not None and tag_id != "":
                tag = Tag.objects.filter(id=tag_id).get()
                TagsToPost.objects.create(post=created_post, tag=tag)
        
        return redirect("user-posts",username)
    form = CreatePostForm()
    return render(request=request, template_name="blog/create_post.html", context={"create_post_form":form})