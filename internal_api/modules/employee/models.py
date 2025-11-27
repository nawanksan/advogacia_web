from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Employee(models.Model):
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
        blank=True,
        null=True,
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
        verbose_name=_('Full Name'),
        max_length=50,
    )
    oab_status: models.CharField = models.CharField(
        verbose_name=_('Full Name'),
        max_length=50,
    )
    specialty: models.CharField = models.CharField(
        verbose_name=_('Full Name'),
        max_length=50,
    )
    role: models.ForeignKey = models.ForeignKey(
        to='employee.Role',
        on_delete=models.RESTRICT,
        verbose_name=_('Role'),
        related_name='employee_role_role',
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['full_name']
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self) -> str:
        return f'{self.full_name} - {self.role.description}'


class Role(models.Model):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=50
    )
    description: models.CharField = models.CharField(
        verbose_name=_('Description')
    )


    class Meta:
        ordering = ['-id']
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self) -> str:
        return str(self.description)