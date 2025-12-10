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
    is_admin_ti: models.BooleanField = models.BooleanField(
        verbose_name=_('TI Admin Status'),
        default=False,
        help_text=_(
            'Designates that the user has access to IT permissions assignment management.'
        ),
    )
    is_admin: models.BooleanField = models.BooleanField(
        verbose_name=_('Admin Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into the admin site.'
        ),
    )
    is_active: models.BooleanField = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        user: str = (
            self.username if (self.is_admin or not self.employee) else
            f'{self.username} - {self.employee.full_name}'
        )
        return user
    
    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
