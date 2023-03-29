from django.contrib import admin

from .models import Subreddit, Post, Comment


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image', 'created', 'created_by']
    prepopulated_fields = {'slug': ('name',)}  # llena automaticamente slug, cuando se rellena title
    raw_id_fields = ['created_by']  # Crea una barra de busqueda en el campo


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'publish', 'status',
                    'subreddit', 'author']
    prepopulated_fields = {'slug': ('title',)}  # llena automaticamente slug, cuando se rellena title
    raw_id_fields = ['subreddit', 'author']  # Crea una barra de busqueda en el campo


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created', 'active', 'is_parent']
    raw_id_fields = ['post', 'author']  # Crea una barra de busqueda en el campo
