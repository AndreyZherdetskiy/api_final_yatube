from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение: только автор может изменять/удалять, остальные — только читать."""

    def has_object_permission(self, request: Request, view: View, obj: object) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
