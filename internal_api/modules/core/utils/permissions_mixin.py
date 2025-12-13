from django.conf import settings
from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from axes.models import AccessAttempt, AccessLog, AccessFailureLog


class CustomAdminSite(admin.AdminSite):
    """
    Customiza o site de administração do Django.
    """

    site_header = 'SIGSN Admin'
    site_title = 'SIGSN Admin'

    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = self.site_header
        context['site_title'] = self.site_title
        return context

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        reorder = settings.ADMIN_REORDER
        if not reorder:
            return app_list

        reordered = []
        remaining_models = {
            f"{app['app_label']}.{model['object_name']}".lower(): model
            for app in app_list
            for model in app['models']
        }

        used_models = set()

        for group in reorder:
            app_models = []
            for entry in group["models"]:
                if isinstance(entry, dict):
                    model_path = entry["model"].lower()
                    label = entry.get("label")
                else:
                    model_path = entry.lower()
                    label = None

                model = remaining_models.get(model_path)
                if model:
                    model = model.copy()
                    if label:
                        model["name"] = label
                    app_models.append(model)
                    used_models.add(model_path)

            if app_models:
                reordered.append({
                    "name": group["label"],
                    "app_label": group["app"],
                    "models": app_models
                })

        # adiciona modelos não utilizados (para não sumirem do admin)
        unused_models = [
            model for key, model in remaining_models.items()
            if key not in used_models
        ]
        if unused_models:
            reordered.append({
                "name": "Outros",
                "app_label": "outros",
                "models": unused_models
            })

        return reordered


admin_site = CustomAdminSite(name='custom_admin')

class ReadModifyOnly(admin.ModelAdmin):
    """
    Classe base para modelos que só podem ser lidos ou modificados, mas não excluídos.
    """

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


class BaseAdminPermission(admin.ModelAdmin):
    module_slug: str = None
    submodule_slug: str = None
    permissions_actions = ('visualizar', 'adicionar', 'editar', 'desativar')

    def has_permission(self, request, action):
        if request.user.is_superuser:
            return True

        if not hasattr(request.user, 'custom_permissions'):
            return False

        modules = self.module_slug if isinstance(self.module_slug, (list, tuple)) else [self.module_slug or '']
        submodules = self.submodule_slug if isinstance(self.submodule_slug, (list, tuple)) else [self.submodule_slug or '']
        action_slug = action

        for module in modules:
            for submodule in submodules:
                perms = request.user.custom_permissions.filter(
                    module__description=module,
                    submodule=submodule,
                )
                for perm in perms:
                    if perm.actions.filter(description=action_slug).exists():
                        return True
        return False

    def has_view_permission(self, request, obj=None):
        result = self.has_permission(request, 'visualizar')
        return result

    def has_add_permission(self, request):
        return self.has_permission(request, 'adicionar')

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, 'editar')

    def has_delete_permission(self, request, obj=None):  # noqa: PLR6301
        return False

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)

        # aqui junta sua permissão customizada, mas só habilita se usuário for staff e tiver permissão Django padrão
        has_custom_perm = self.has_permission(request, 'visualizar')
        has_django_perm = (
            perms.get('view', False)
            and request.user.is_staff
            and request.user.is_active
        )
        perms.update({
            'view': has_custom_perm and has_django_perm,
            'add': has_custom_perm and perms.get('add', False),
            'change': has_custom_perm and perms.get('change', False),
            'delete': has_custom_perm and perms.get('delete', False),
        })
        return perms

    def has_module_permission(self, request):
        result = self.has_permission(request, 'visualizar')
        return result


admin_site.register(AccessAttempt, ReadModifyOnly)
admin_site.register(AccessLog, ReadModifyOnly)
admin_site.register(AccessFailureLog, ReadModifyOnly)
