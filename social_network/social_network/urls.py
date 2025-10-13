from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, AddCommentToPostView, UpdateAndDestroyCommentView, LikePostView

router = SimpleRouter()
router.register(r'api/v1/posts', PostViewSet, basename='posts')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/posts/<int:post_id>/comments', AddCommentToPostView.as_view(), name='add_comment'),
                  path('api/v1/comments/<int:pk>', UpdateAndDestroyCommentView.as_view(), name='update_comment'),
                  path('api/v1/posts/<int:post_id>/like', LikePostView.as_view(), name='like'),
                  path('', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
