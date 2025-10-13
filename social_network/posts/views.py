from rest_framework import viewsets

from posts.models import Post
from posts.permissions import IsOwnerOrReadonly
from posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

# class PostsListCreateView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsOwnerOrReadonly]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class RetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsOwnerOrReadonly]
#
#     def perform_update(self, serializer):
#         serializer.save(author=self.request.user)
