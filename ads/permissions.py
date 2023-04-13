from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Selection
from users.models import User


class SelectionUpdatePermissions(BasePermission):
    massage = 'It is forbidden to update a selection that is not your own'

    def has_permission(self, request, view):
        try:
            entity = Selection.objects.get(pk=view.kwargs["pk"]) # выводим все подборки
        except Selection.DoesNotExist:
            raise Http404
        # сравниваем какой ввел пользователь и какой селект мы хотим изменить
        if request.user.id == entity.owner_id or request.user.role in ["member", "admin"]:
            return True
        return False
