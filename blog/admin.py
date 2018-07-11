from django.contrib import admin
from .models import Post, Comment, AppPreferrence, PostPreferrence

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(AppPreferrence)
admin.site.register(PostPreferrence)
