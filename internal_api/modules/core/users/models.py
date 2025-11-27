from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Users(models.Model):
    cpf: models.CharField = models.CharField(
        verbose_name=_('CPF'),
        max_length=11
    )
    full_name: models.CharField = models.CharField(
        verbose_name=_('Full Name'),
        max_length=70
    )
    email: models.CharField = models.CharField(
        verbose_name=_('Email')
    )