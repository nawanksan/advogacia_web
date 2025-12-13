from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmployeeConfig(AppConfig):
    """
    Responsável por configurar o submódulo de resgistro,
    para o Django reconhecer como um app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'internal_api.modules.employee'
    verbose_name = _('Employee')

    def ready(self):
        pass
