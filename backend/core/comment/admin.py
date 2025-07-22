from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'author','body', 'edited', 'created', 'updated')
    list_filter = ('edited', 'created', 'author', 'post')
    search_fields = ('body', 'author__email', 'author__username',)
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')