from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Like
from django.contrib import messages
from .forms import PostUpdateCreateForm, CommentCreateForm, CommentReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SearchForm

class HomeView(View):
    def get(self, request):
        form = SearchForm()
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/home.html', {'posts': posts, 'form': form})

class PostDetailView(View):
    from_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/details.html', {'post': self.post_instance, 'comments': comments, 'form':self.from_class, 'reply_form':self.form_class_reply, 'can_like':can_like})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.post_instance
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Comment saved', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
        return render(request, 'home/details.html', {'post': self.post_instance, 'form':self.from_class()})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
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
        self.post_instance = get_object_or_404(Post, id=kwargs['post_id'])
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

class PostReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request,post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'Comment replied successfully','success')
        return redirect('home:post_detail', post.id, post.slug)

class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post, user=request.user)
        if likes.exists():
            messages.error(request, 'You already liked this post', 'error')
        else:
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'Post liked successfully','success')
        return redirect('home:post_detail', post.id, post.slug)

















