from django.db import models
from django.utils.translation import gettext_lazy as _
from advogacia_web.internal_api.modules.core.main.models import AbstractBaseModel

class Address(AbstractBaseModel):
    street_name: models.CharField = models.CharField(
        verbose_name=_('Street Name'),
        max_length=100
    )
    number: models.PositiveIntegerField = models.PositiveIntegerField(
        verbose_name=_('Number')
    )
    postal_code: models.CharField = models.CharField(
        verbose_name=_('Postal Code')
    )
    complements: models.TextField = models.TextField(
        verbose_name=_('Complements'),
        null=True,
        blank=True
    )
    
    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self) -> str:
        return f'{self.street_name} - {self.number} - {self.neighborhood.name} - {self.neighborhood.city.name} - {self.neighborhood.city.federative_unit.abbreviation} - {self.neighborhood.city.federative_unit.country.abbreviation}'