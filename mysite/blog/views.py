from typing import Any
from django.shortcuts import render
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
        context["maxCom"] = kwargs["new_max"]
        context["comments"] = Comment.objects.filter(post_id=post_id).order_by("created_on")[:context["maxCom"]]
        return context
    
    def get(self, request, slug):
        self.object = self.get_object()
        if "maxCom" in request.GET:
            new_max = int(request.GET["maxCom"]) + 10
        else:
            new_max = 10
        context = self.get_context_data(object=self.object, new_max=new_max)
        return render(request, self.template_name, context=context)