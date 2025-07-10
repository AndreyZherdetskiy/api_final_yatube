from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

from posts.constants import (
    GROUP_TITLE_MAX_LENGTH,
    NO_SELF_FOLLOW_CONSTRAINT,
    RELATED_NAME_COMMENTS,
    RELATED_NAME_FOLLOWER,
    RELATED_NAME_FOLLOWING,
    RELATED_NAME_POSTS,
    STR_CREATED,
    STR_PUB_DATE,
    UNIQUE_FOLLOW_CONSTRAINT
)


User = get_user_model()


class Group(models.Model):
    """
    Модель группы.

    Attributes:
        title (str): Название группы.
        slug (str): Уникальный slug-идентификатор группы.
        description (str): Описание группы.
    """

    title = models.CharField(max_length=GROUP_TITLE_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """
    Модель поста.

    Attributes:
        text (str): Текст поста.
        pub_date (datetime): Дата публикации поста.
        author (User): Автор поста.
        image (ImageField): Изображение, прикрепленное к посту.
        group (Group): Группа, к которой относится пост.
    """

    text = models.TextField()
    pub_date = models.DateTimeField(STR_PUB_DATE, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RELATED_NAME_POSTS)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name=RELATED_NAME_POSTS,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """
    Модель комментария.

    Attributes:
        author (User): Автор комментария.
        post (Post): Пост, к которому относится комментарий.
        text (str): Текст комментария.
        created (datetime): Дата создания комментария.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RELATED_NAME_COMMENTS)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name=RELATED_NAME_COMMENTS)
    text = models.TextField()
    created = models.DateTimeField(STR_CREATED, auto_now_add=True, db_index=True)


class Follow(models.Model):
    """
    Модель подписки.

    Attributes:
        user (User): Пользователь, который подписан.
        following (User): Пользователь, на которого подписаны.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RELATED_NAME_FOLLOWING)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=RELATED_NAME_FOLLOWER
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'following'], name=UNIQUE_FOLLOW_CONSTRAINT),
            CheckConstraint(check=~Q(user=models.F('following')), name=NO_SELF_FOLLOW_CONSTRAINT),
        ]
