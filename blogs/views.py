from django.shortcuts import render
from .models import BlogPost

def blog_post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blogs/blog_post_list.html', {'posts': posts})

def blog_post_detail(request, pk):
    post = BlogPost.objects.get(pk=pk)
    return render(request, 'blogs/blog_post_detail.html', {'post': post})

# Create your views here.
