from django.shortcuts import render
from django.views import generic
from .models import Post
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