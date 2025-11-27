from django.apps import AppConfig
# from django.utils.translation import gettext_lazy as _


class CaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "internal_api.modules.case"
    # verbose_name = _('Cases')
