from typing import Any
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic
from .models import Post
from user.models import Comment
# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class PostDetail(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        post_id = context["post"].id
        context["comments_len"] = len(Comment.objects.filter(post_id=post_id).order_by("created_on"))
        return context
    
    def get(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context=context)
    
def post_comments(request, post_id):
        if request.method == "GET":
            maxCom = int(request.GET.get("maxCom"))
            comments = Comment.objects.filter(post_id=post_id).order_by("created_on")
            if (maxCom-1 >= len(comments)):
                maxCom = len(comments)
            context = {"comments" : Comment.objects.filter(post_id=post_id).order_by("created_on")[:maxCom]};
            return render(request,"blog/post_comments.html", context=context)
        return HttpResponse("Error. No get request")