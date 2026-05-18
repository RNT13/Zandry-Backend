from rest_framework.permissions import BasePermission


class IsCompanyUser(BasePermission):
    """Permite acesso apenas para usuários autenticados com company vinculada."""

    message = "Usuário sem empresa vinculada."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "company_id", None))
