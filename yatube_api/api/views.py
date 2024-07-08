from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer,
                             FollowSerializer,
                             GroupSerializer,
                             PostSerializer)
from posts.models import Group, Post


class BaseViewSet(viewsets.ModelViewSet):
    """
    Базовый ViewSet, содержащий общую логику.

    Attributes:
        permission_classes (tuple): Набор разрешений для данного ViewSet.
    """

    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)


class PostViewSet(BaseViewSet):
    """
    ViewSet для работы с постами.

    Attributes:
        queryset (QuerySet): Набор объектов модели Post.
        serializer_class (serializer): Сериализатор для модели Post.
        pagination_class (LimitOffsetPagination): Класс пагинации для постов.
        filter_backends (tuple): Набор фильтров для постов.
        filterset_fields (tuple): Поля, по которым можно фильтровать посты.
        ordering_fields (tuple): Поля, по которым можно сортировать посты.
        search_fields (tuple): Поля, по которым можно искать посты.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ('author', 'group', 'pub_date',)
    ordering_fields = ('author', 'pub_date',)
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
        filter_backends (tuple): Набор фильтров для комментариев.
        filterset_fields (tuple): Поля, по которым можно фильтровать
        комментарии.
        ordering_fields (tuple): Поля, по которым можно сортировать
        комментарии.
        ordering (str): Порядок сортировки комментариев.
        search_fields (tuple): Поля, по которым можно искать комментарии.
    """

    serializer_class = CommentSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ('author', 'post', 'created',)
    ordering_fields = ('author', 'post', 'created',)
    ordering = ('created',)
    search_fields = ('__all__',)

    def get_queryset(self):
        """
        Возвращает все комментарии, связанные с определенным постом.
        Использует post_id из URL-адреса.
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
        permission_classes (tuple): Набор разрешений для данного ViewSet.
        filter_backends (tuple): Набор фильтров для подписок.
        search_fields (tuple): Поля, по которым можно искать подписки.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает все подписки текущего пользователя."""
        return self.request.user.following.all()

    def perform_create(self, serializer):
        """
        Сохраняет новую подписку.
        Устанавливает пользователя, который подписывается,
        как текущего пользователя.
        """
        serializer.save(user=self.request.user)


class GroupViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet для работы с группами.

    Attributes:
        queryset (QuerySet): Набор объектов модели Group.
        serializer_class (serializer): Сериализатор для модели Group.
        permission_classes (tuple): Набор разрешений для данного ViewSet.
        filter_backends (tuple): Набор фильтров для групп.
        filterset_fields (tuple): Поля, по которым можно фильтровать группы.
        ordering_fields (tuple): Поля, по которым можно сортировать группы.
        ordering (str): Порядок сортировки групп.
        search_fields (tuple): Поля, по которым можно искать группы.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_fields = ('slug', 'title',)
    ordering_fields = ('slug', 'title',)
    ordering = ('title',)
    search_fields = ('__all__',)
