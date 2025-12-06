from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_active: models.BooleanField = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
    )
    last_modification: models.DateTimeField =  models.DateTimeField(
        verbose_name=_("Last Modification"),
        auto_now=True,
    )
    registration: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Registration Date"),
        auto_now_add=True,
    )
    # last_user

    class Meta:
        abstract = True