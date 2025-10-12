from django.contrib import admin
from .models import Post, Comment, Like

admin.site.register(Like)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    list_filter = ('updated',)
    search_fields = ('body', 'slug')
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'is_reply')
    list_filter = ('created','is_reply')
    search_fields = ('body',)
    raw_id_fields = ('user','post', 'reply')