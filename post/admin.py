from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at']
    list_filter = ['created_at']
    ordering = ['-created_at']
    search_fields = ['content', 'user__username']

admin.site.register(Post, PostAdmin)