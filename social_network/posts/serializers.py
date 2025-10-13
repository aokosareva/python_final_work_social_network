from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, Comment, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']

        return super().create(validated_data)


class CommentInPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'text', 'commented_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentInPostSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField(method_name='get_likes_count')
    image = serializers.ImageField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.reactions.count()
