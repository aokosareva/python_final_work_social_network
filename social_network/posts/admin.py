from django.contrib import admin

from posts.models import Post, PostImage, Comment, Reaction

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(Reaction)
