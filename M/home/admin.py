from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    list_filter = ('updated',)
    search_fields = ('body', 'slug')
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)

