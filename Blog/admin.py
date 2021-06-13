from django.contrib import admin
from .models import Post, prod, actors
# Register your models here.
# admin.site.register(Post)
admin.site.register(prod)
admin.site.register(actors)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'actors', 'description', 'slug', 'publish', 'author')
    list_filter = ('title', 'producer', 'actors', 'description', 'slug', 'publish', 'author')
    search_fields = ('title', 'producer')
# Register your models here.
