from django.contrib import admin
from .models import Post, Comment, AppPreferrence, PostPreferrence, ReplyToComment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(AppPreferrence)
admin.site.register(PostPreferrence)
admin.site.register(ReplyToComment)
