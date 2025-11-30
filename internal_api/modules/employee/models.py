from django.db import models
from django.utils.translation import gettext_lazy as _
from internal_api.modules.core.main.models import AbstractBaseModel
from internal_api.modules.core.utils.choices import OAB_STATUS_CHOICES, TYPE_USER_EMPLOYER_CHOICES


# Create your models here.
class Employee(AbstractBaseModel):
    full_name: models.CharField = models.CharField(
        verbose_name=_('Full Name'),
        max_length=70,
    )
    cpf: models.CharField = models.CharField(
        verbose_name=_('CPF'),
        max_length=11,
        unique=True,
    )
    email: models.EmailField = models.EmailField(
        verbose_name=_('Email'),
        unique=True,
    )
    birth_date: models.DateField = models.DateField(
        verbose_name=_('Birth Date'),
    )
    cellphone: models.CharField = models.CharField(
        verbose_name=_('Cellphone'),
        max_length=11,
        null=True,
        blank=True,
    )
    oab: models.CharField = models.CharField(
        verbose_name=_('OAB'),
        max_length=50,
        null=True,
        blank=True
    )
    oab_status: models.CharField = models.CharField(
        verbose_name=_('OAB Status'),
        choices=OAB_STATUS_CHOICES,
        max_length=2,
        null=True,
        blank=True,
    )
    specialty: models.CharField = models.CharField(
        verbose_name=_('Epecialty'),
        max_length=50,
        null=True,
        blank=True
    )
    type: models.CharField = models.CharField(
        choices=TYPE_USER_EMPLOYER_CHOICES,
        max_length=2,
        default='CL',
    )
    address: models.ForeignKey = models.ForeignKey(
        to='address.Address',
        on_delete=models.RESTRICT,
        verbose_name=_('Address'),
        related_name='employee_address_address',
        null=True,
        blank=True
    )
    role: models.ForeignKey = models.ForeignKey(
        to='employee.Role',
        on_delete=models.RESTRICT,
        verbose_name=_('Role'),
        related_name='employee_role_role',
        null=True,
        blank=True
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['full_name']
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self) -> str:
        return f'{self.full_name} - {self.role.description if self.role else ""}'


class Role(AbstractBaseModel):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=50
    )
    description: models.CharField = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        blank=True,
    )


    class Meta:
        ordering = ['-id']
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self) -> str:
        return str(self.description)