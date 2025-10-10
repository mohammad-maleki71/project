from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib import messages
from .forms import PostUpdateCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home/details.html', {'post': post})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully','success')
        else:
            messages.error(request, 'Post not deleted','error')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs ):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post updated successfully','success')
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form': form})

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm
    template_name = 'home/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post created successfully','success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
        return render(request, self.template_name, {'form': form})

















