from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.permissions import BasePermission

from core.utils.constants import PERMISSIONS_IT


class BaseAccess(BasePermission):
    """
    Responsável por o modelo o qual as classes que implementam
    regras de acesso a rotas devem seguir.
    """

    message: str = str(_('You do not have permission to perform this action.'))

    MODULE_DESCRIPTION: str
    PERMISSION_DESCRIPTION: str
    ACTION_DESCRIPTION: str

    def has_permission(
        self, request: HttpRequest, controller: ControllerBase
    ) -> bool:
        if request.user.is_superuser:
            return True

        if not request.user.is_admin_it and (
            self.MODULE_DESCRIPTION == 'tecnologia-informacao'
            and self.PERMISSION_DESCRIPTION in PERMISSIONS_IT
        ):
            return False

        user_role = request.user.employee.role

        module_set = set()
        permission_set = set()
        action_set = set()

        role_permissions = user_role.rolepermission_role_role.all()

        for role_permission in role_permissions:
            module = role_permission.permission.module.description
            module_set.add(module)

            if module != self.MODULE_DESCRIPTION:
                continue

            permission = role_permission.permission.description
            permission_set.add(permission)

            if permission != self.PERMISSION_DESCRIPTION:
                continue

            actions = role_permission.actions.all()
            for action in actions:
                action_set.add(action.description)

        return (
            self.PERMISSION_DESCRIPTION in permission_set
            and self.ACTION_DESCRIPTION in action_set
        )


class UserPermissionService:
    """
    Serviço responsável por obter e manipular permissões e ações
    associadas ao usuário autenticado.
    """

    def __init__(self, user):
        """
        Inicializa o serviço com o usuário autenticado.
        """
        self.user = user
        self.modules = {}
        self._load_permissions()

    # =========================
    # Métodos principais
    # =========================

    def _load_permissions(self):
        user = self.user

        if user.is_superuser:
            self.modules = {"*": {"*": ["*"]}}
            return

        user_role = getattr(user, "employee", None)
        if not user_role or not hasattr(user_role, "role"):
            self.modules = {}
            return

        role_permissions = user.employee.role.rolepermission_role_role.all()

        for role_permission in role_permissions:
            module = role_permission.permission.module.description
            permission = role_permission.permission.description
            actions = [a.description for a in role_permission.actions.all()]

            if module not in self.modules:
                self.modules[module] = {}

            if permission not in self.modules[module]:
                self.modules[module][permission] = set()

            self.modules[module][permission].update(actions)

        for module in self.modules:
            for permission in self.modules[module]:
                self.modules[module][permission] = list(
                    self.modules[module][permission]
                )

    def to_dict(self):
        return self.modules

    def has_module(self, module_description: str) -> bool:
        """
        Verifica se o usuário tem acesso a um módulo específico.
        """
        return module_description in self.modules or "*" in self.modules

    def has_permission(
        self,
        module_description: str,
        permission_description: str
    ) -> bool:
        """
        Verifica se o usuário possui uma permissão específica.
        """
        return (
            module_description
            in self.modules and permission_description
            in self.modules[module_description]
        )

    def has_action(
        self,
        module_description: str,
        permission_description: str,
        action_description: str
    ) -> bool:
        """
        Verifica se o usuário possui uma ação específica.
        """
        return (
            self.has_permission(module_description, permission_description)
            and action_description
            in self.modules[module_description][permission_description]
        )

    def has_access(self, module: str, permission: str, action: str) -> bool:
        """
        Verifica se o usuário tem acesso completo a um conjunto
        (módulo, permissão e ação).
        """
        return (
            self.has_module(module)
            and self.has_permission(module, permission)
            and self.has_action(module, permission, action)
        )
