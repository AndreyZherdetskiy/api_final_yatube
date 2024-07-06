from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Пользовательское разрешение.

    Разрешение дает доступ:
    - на чтение для всех методов.
    - на изменение и удаление только автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
