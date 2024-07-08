from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Attributes:
        author (serializers.SlugRelatedField): Поле для автора поста,
        извлекается из связанной модели User.
        image (serializers.ImageField): Поле для изображения поста,
        необязательное.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Attributes:
        title (str): Название группы.
        slug (str): Уникальный slug-идентификатор группы.
        description (str): Описание группы.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Attributes:
        author (serializers.SlugRelatedField): Поле для автора комментария,
        извлекается из связанной модели User.
        post (serializers.PrimaryKeyRelatedField): Поле для поста,
        к которому относится комментарий, доступно только для чтения.
        text (str): Текст комментария.
        created (datetime): Дата создания комментария.
    """

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.

    Attributes:
        user (serializers.SlugRelatedField): Поле для пользователя,
        который подписан.
        following (serializers.SlugRelatedField): Поле для пользователя,
        на которого подписаны.
    """

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='You already follow this user'
            )
        ]

    def validate_following(self, value):
        """
        Проверяет, что пользователь не пытается подписаться
        на самого себя.
        """
        if value == self.context['request'].user:
            raise serializers.ValidationError('You cannot follow yourself')
        return value
