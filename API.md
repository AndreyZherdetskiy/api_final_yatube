# Документация API Yatube

## Аутентификация

### Получение JWT-токена
**POST** `/api/v1/jwt/create/`

**Request:**
```json
{
  "username": "user",
  "password": "string"
}
```
**Response:**
```json
{
  "access": "<token>",
  "refresh": "<token>"
}
```

### Обновление JWT-токена
**POST** `/api/v1/jwt/refresh/`

**Request:**
```json
{
  "refresh": "<token>"
}
```
**Response:**
```json
{
  "access": "<token>"
}
```

---

## Посты

### Получить список постов
**GET** `/api/v1/posts/`

**Response:**
```json
[
  {
    "id": 1,
    "author": "user",
    "text": "Текст поста",
    "pub_date": "2024-01-01T12:00:00Z",
    "group": 1
  }
]
```

### Создать пост
**POST** `/api/v1/posts/`

**Request:**
```json
{
  "text": "Новый пост",
  "group": 1
}
```
**Response:**
```json
{
  "id": 2,
  "author": "user",
  "text": "Новый пост",
  "pub_date": "2024-01-02T12:00:00Z",
  "group": 1
}
```

### Получить/обновить/удалить пост
**GET/PATCH/DELETE** `/api/v1/posts/{post_id}/`

---

## Комментарии

### Получить комментарии к посту
**GET** `/api/v1/posts/{post_id}/comments/`

**Response:**
```json
[
  {
    "id": 1,
    "author": "user",
    "text": "Комментарий",
    "created": "2024-01-01T13:00:00Z"
  }
]
```

### Создать комментарий
**POST** `/api/v1/posts/{post_id}/comments/`

**Request:**
```json
{
  "text": "Новый комментарий"
}
```
**Response:**
```json
{
  "id": 2,
  "author": "user",
  "text": "Новый комментарий",
  "created": "2024-01-02T13:00:00Z"
}
```

### Получить/обновить/удалить комментарий
**GET/PATCH/DELETE** `/api/v1/posts/{post_id}/comments/{comment_id}/`

---

## Группы

### Получить список групп
**GET** `/api/v1/groups/`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Группа 1",
    "description": "Описание группы"
  }
]
```

### Получить группу
**GET** `/api/v1/groups/{group_id}/`

---

## Подписки

### Получить список подписок
**GET** `/api/v1/follow/`

**Response:**
```json
[
  {
    "user": "user",
    "following": "author"
  }
]
```

### Подписаться на пользователя
**POST** `/api/v1/follow/`

**Request:**
```json
{
  "following": "author"
}
```
**Response:**
```json
{
  "user": "user",
  "following": "author"
}
```
