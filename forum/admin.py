from django.contrib import admin
from django.contrib import admin
from .models import PostModel, LikeModel, CommentModel


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at')  
    
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'post', 'user',)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'created_at') 
  
 
admin.site.register(PostModel, PostModelAdmin)
admin.site.register(LikeModel, LikeModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)