from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from internal_api.modules.core.users.user_manager import CustomUserManager


class CustomUsers(AbstractBaseUser, PermissionsMixin):
    username: models.CharField = models.CharField(
        verbose_name=_('Username'),
        max_length=60,
        unique=True,
    )
    date_joined: models.DateTimeField = models.DateTimeField(
        verbose_name=_('Join Date'),
        auto_now_add=True,
    )
    employee: models.OneToOneField = models.OneToOneField(
        to='employee.Employee',
        blank=True,
        null=True,
        verbose_name=_('Employee User'),
        related_name='user_employee_employee',
        on_delete=models.RESTRICT,
    )
    is_active: models.BooleanField = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
