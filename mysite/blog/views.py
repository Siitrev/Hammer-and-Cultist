from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic
from django.http import HttpRequest, HttpResponse
from .models import Post, Tag
from .forms import CreatePostForm
from user.models import Comment
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from .handle_file import save_file
import json
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
            post_list = Post.objects.all()
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

def create_post(request : HttpRequest, username : str):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.files)
            img = form.files["image"]
            try:
                save_file(img)
            except ValidationError as e:
                form.add_error("image", e)
                return render(request=request, template_name="blog/create_post.html", context={"create_post_form" : form})
            return render(request=request, template_name="blog/create_post.html", context={"create_post_form" : form})
    form = CreatePostForm()
    return render(request=request, template_name="blog/create_post.html", context={"create_post_form":form})