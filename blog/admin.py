from django.contrib import admin
from .models import Post, Comment, AppPreferrence, PostPreferrence, ReplyToComment, Cluster


class PostAdmin(admin.ModelAdmin):
      readonly_fields = ('id', )

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, PostAdmin)
admin.site.register(AppPreferrence)
admin.site.register(PostPreferrence)
admin.site.register(ReplyToComment)

admin.site.register(Cluster, ClusterAdmin)