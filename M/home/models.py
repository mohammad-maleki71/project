from django.db import models
from account.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.slug}, {self.updated.strftime("%B %d, %Y")}'

    class Meta:
        ordering = ['-created', 'body']

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f'{self.user} {self.body[:30]}'

    class Meta:
        ordering = ['-created', 'body']