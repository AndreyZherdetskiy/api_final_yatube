"""constants.py — константы для модуля posts."""

# related_name для моделей
RELATED_NAME_POSTS = 'posts'
RELATED_NAME_COMMENTS = 'comments'
RELATED_NAME_FOLLOWING = 'following'
RELATED_NAME_FOLLOWER = 'follower'

# Строковые литералы для моделей
STR_PUB_DATE = 'Дата публикации'
STR_CREATED = 'Дата добавления'

# Имена ограничений
UNIQUE_FOLLOW_CONSTRAINT = 'unique_follow'
NO_SELF_FOLLOW_CONSTRAINT = 'no_self_follow'

# Ограничения длины
GROUP_TITLE_MAX_LENGTH = 200
