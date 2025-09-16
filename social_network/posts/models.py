from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Post(models.Model):
    class Meta:
        db_table = 'posts_posts'

    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    geo_data = models.JSONField(null=True)


class PostImage(models.Model):
    class Meta:
        db_table = 'posts_images'

    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Reaction(models.Model):
    class Meta:
        db_table = 'posts_reactions'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reacted_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    class Meta:
        db_table = 'posts_comments'

    text = models.TextField(max_length=500)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)
