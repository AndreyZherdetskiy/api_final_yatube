from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from posts.models import Follow, Group, Post

User = get_user_model()


class BaseViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet, содержащий общую логику.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)


class PostViewSet(BaseViewSet):
    """
    ViewSet для работы с постами.

    Attributes:
        queryset (QuerySet): Набор объектов модели Post.
        serializer_class (serializer): Сериализатор для модели Post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    filterset_fields = ('author', 'group', 'pub_date',)
    ordering_fields = ('author', 'pub_date',)
    ordering = ('-pub_date',)
    search_fields = ('author__username', 'group', 'pub_date', 'text',)

    def perform_create(self, serializer):
        """
        Сохраняет новый пост.
        Устанавливает автора как текущего пользователя.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(BaseViewSet):
    """
    ViewSet для работы с комментариями.

    Attributes:
        serializer_class (serializer): Сериализатор для модели Comment.
    """

    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ('author', 'post', 'created',)
    ordering_fields = ('author', 'post', 'created',)
    ordering = ('created',)
    search_fields = ('__all__',)

    def get_queryset(self):
        """
        Возвращает все комментарии, связанные с определенным постом,
        используя post_id из URL-адреса.
        Предварительно проверяет, что запрошенный пост существует.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Сохраняет новый комментарий.
        Устанавливает автора как текущего пользователя
        и связывает комментарий с постом, используя post_id из URL-адреса.
        Предварительно проверяет, что запрошенный пост существует.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet для работы с подписками.

    Attributes:
        serializer_class (serializer): Сериализатор для модели Follow.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """
        Возвращает все подписки текущего пользователя.
        Если пользователь анонимный, возвращает пустой набор.
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Сохраняет новую подписку.
        Устанавливает пользователя, который подписывается,
        как текущего пользователя.
        Проверяет, что пользователь не пытается подписаться на самого себя
        и что такая подписка еще не существует.
        """
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_404_NOT_FOUND)

        following = serializer.validated_data['following']
        if self.request.user == following:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Follow.objects.filter(user=self.request.user, following=following).exists():
            return Response(
                {'error': 'You already follow this user'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(user=self.request.user)


class GroupViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet для работы с группами.

    Attributes:
        queryset (QuerySet): Набор объектов модели Group.
        serializer_class (serializer): Сериализатор для модели Group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ('slug', 'title',)
    ordering_fields = ('slug', 'title',)
    ordering = ('title',)
    search_fields = ('__all__',)
