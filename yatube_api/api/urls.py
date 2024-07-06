from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet, PostViewSet, FollowViewSet, GroupViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
