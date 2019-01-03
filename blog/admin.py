from django.contrib import admin
from .models import Post, Comment, AppPreferrence, PostPreferrence, ReplyToComment, Cluster
from .models import PollQuestions, PollAnswer

class PostAdmin(admin.ModelAdmin):
      readonly_fields = ('id', )

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

class PollAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ['post']
    
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, PostAdmin)
admin.site.register(AppPreferrence)
admin.site.register(PostPreferrence)
admin.site.register(ReplyToComment)

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(PollQuestions, PollAdmin)
admin.site.register(PollAnswer, PollAdmin)