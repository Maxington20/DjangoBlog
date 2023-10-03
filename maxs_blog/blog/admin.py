# Register your models here.
from django.contrib import admin
from .models import Post
from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    form = PostForm

admin.site.register(Post, PostAdmin)