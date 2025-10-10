from django.shortcuts import render, redirect
from django.views import View
from home.models import Post
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home/details.html', {'post': post})

class PostDeleteView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully','success')
        else:
            messages.error(request, 'Post not deleted','error')
        return redirect('home:home')


