from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    class Meta:
        db_table = 'posts_posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    text = models.TextField()
    image = models.ImageField(upload_to='images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # geo_data = models.JSONField(null=True)

    def __str__(self):
        return f"{self.author} - {self.text[:20]}"

class Reaction(models.Model):
    class Meta:
        db_table = 'posts_reactions'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reacted_at.strftime('%Y-%m-%d %H:%I:%S')} - {self.author} to post #{self.post.pk}"


class Comment(models.Model):
    class Meta:
        db_table = 'posts_comments'

    text = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commented_at.strftime('%Y-%m-%d %H:%I:%S')} - {self.commenter} to post #{self.post.pk}"
