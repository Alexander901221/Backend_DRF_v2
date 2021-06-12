from rest_framework.permissions import BasePermission


# Проверка на то что аккаунт подтвержден ( confirm_email == True )
class AccountIsVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.confirm_email)
