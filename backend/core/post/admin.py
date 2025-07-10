from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'edited', 'created', 'updated')
    list_filter = ('edited', 'created', 'author')
    search_fields = ('body', 'author__email', 'author__username')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')