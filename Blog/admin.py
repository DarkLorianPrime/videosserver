from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'actors', 'description', 'slug', 'publish', 'author')
    list_filter = ('title', 'producer', 'actors', 'description', 'slug', 'publish', 'author')
    search_fields = ('title', 'producer')
