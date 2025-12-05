from django.db import models
from django.utils.translation import gettext_lazy as _
from internal_api.modules.core.main.models import AbstractBaseModel

class Country(AbstractBaseModel):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=30
    )
    abbreviation: models.CharField = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=3
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('Country')
        verbose_name_plural = _('Countrys')

    def __str__(self):
        return f'{self.name} - {self.abbreviation}'

class FederativeUnit(AbstractBaseModel):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=30
    )
    abbreviation: models.CharField = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=2
    )
    country: models.ForeignKey = models.ForeignKey(
        to='address.Country',
        on_delete=models.RESTRICT,
        verbose_name=_('Country'),
        related_name='federativeunit_country_country',
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('FederativeUnit')
        verbose_name_plural = _('FederativeUnits')

    def __str__(self):
        return f'{self.name} - {self.country.abbreviation}'

class City(AbstractBaseModel):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=30
    )
    federative_unit: models.ForeignKey = models.ForeignKey(
        to='address.FederativeUnit',
        on_delete=models.RESTRICT,
        verbose_name=_('Federative Unit'),
        related_name='city_federativeunit_federative_unit'
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return f'{self.name} - {self.federative_unit.abbreviation} - {self.selfederative_unit.country.abbreviation}'

class Neighbordhood(AbstractBaseModel):
    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=30
    )
    city: models.ForeignKey = models.ForeignKey(
        to='address.City',
        on_delete=models.RESTRICT,
        verbose_name=_('City'),
        related_name='neighbordhood_city_city'
    )

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ['-id']
        verbose_name = _('Neighbordhood')
        verbose_name_plural = _('Neighbordhoods')

    def __str__(self) -> str:
        return f'{self.name} - {self.city.name} - {self.city.federative_unit.abbreviation} - {self.city.federative_unit.country.abbreviation}'

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
    neighbordhood: models.ForeignKey = models.ForeignKey(
        to='address.Neighbordhood',
        on_delete=models.RESTRICT,
        verbose_name=_('Neighbordhood'),
        related_name='address_neighbordhood_neighbordhood'
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