from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from posts.models import Post, Comment, Reaction
from posts.permissions import IsOwnerOrReadonly
from posts.serializers import PostSerializer, CommentSerializer, ReactionSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class AddCommentToPostView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs.get('post_id')
        context['post'] = Post.objects.get(pk=post_id)
        return context

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, *kwargs)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BaseException as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateAndDestroyCommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, *kwargs)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BaseException as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, *kwargs)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BaseException as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikePostView(CreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs.get('post_id')
        context['post'] = Post.objects.get(pk=post_id)
        return context

    def create(self, request, *args, **kwargs):
        try:
            like = Reaction.objects.get(post=kwargs.get('post_id'), author=self.request.user)
            if like:
                return Response()
        except Reaction.DoesNotExist:
            pass

        try:
            super().create(request, *args, *kwargs)
            return Response()
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except BaseException as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
