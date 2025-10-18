from django.contrib import admin
from .models import Post, Comment, Like, FileUpload

admin.site.register(Like)
from django.contrib import admin
from .models import Post, FileUpload

class FileUploadInline(admin.TabularInline):
    model = FileUpload
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'created', 'updated')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug': ('body',)}
    inlines = [FileUploadInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'is_reply')
    list_filter = ('created','is_reply')
    search_fields = ('body',)
    raw_id_fields = ('user','post', 'reply')