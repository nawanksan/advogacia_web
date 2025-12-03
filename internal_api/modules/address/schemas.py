from datetime import date
from typing import List, Optional
from ninja import Field, FilterSchema, ModelSchema, Schema

from internal_api.modules.address.models import Address, City, FederativeUnit, Neighbordhood

class FederativeUnitList(Schema):
    """Schema responsável por listar unidades federativas."""
    id: int = Field(..., description='ID da UF')
    name: str = Field(..., description='Nome')
    acronym: str = Field(..., description='Sigla')


class FederativeUnitFilter(FilterSchema):
    """Filtro para unidades federativas."""
    name: str = Field(
        None,
        q='name__istartswith',
        description='Nome da UF'
    )
    acronym: str = Field(
        None,
        q='acronym__iexact',
        description='Sigla da UF'
    )


class FederativeUnitInPost(ModelSchema):
    """Schema de entrada para criação de UF."""

    class Meta:
        model = FederativeUnit
        exclude = ['id']


class FederativeUnitInPut(ModelSchema):
    """Schema de entrada para edição de UF."""

    class Meta:
        model = FederativeUnit
        exclude = ['id']


class FederativeUnitOut(ModelSchema):
    """Schema de saída de UF."""

    class Meta:
        model = FederativeUnit
        fields = "__all__"


class CityFilter(FilterSchema):
    """Filtro para cidades."""
    name: str = Field(
        None,
        q='name__istartswith',
        description='Nome da cidade'
    )
    federative_unit_id: int = Field(
        None,
        q='federative_unit__id__exact',
        description='ID da UF'
    )


class CityList(Schema):
    """Listagem de cidades."""
    id: int = Field(..., description='ID da cidade')
    name: str = Field(..., description='Nome da cidade')
    federative_unit_name: str = Field(
        ...,
        alias='federative_unit.name',
        description='Nome da unidade federativa'
    )
    federative_unit_acronym: str = Field(
        ...,
        alias='federative_unit.acronym',
        description='Sigla da UF'
    )


class CityInPost(ModelSchema):
    """Entrada para criação de cidade."""

    federative_unit_id: int = Field(..., description='ID da UF')

    class Meta:
        model = City
        exclude = ['id', 'federative_unit']


class CityInPut(ModelSchema):
    """Entrada para edição de cidade."""

    federative_unit_id: int = Field(..., description='ID da UF')

    class Meta:
        model = City
        exclude = ['id', 'federative_unit']


class CityOut(ModelSchema):
    """Saída completa de cidade."""
    federative_unit: FederativeUnitList = Field(..., description='UF')

    class Meta:
        model = City
        fields = "__all__"


class NeighborhoodFilter(FilterSchema):
    """Filtro para bairros."""
    name: str = Field(
        None,
        q='name__istartswith',
        description='Nome do bairro'
    )
    city_id: int = Field(
        None,
        q='city__id__exact',
        description='ID da cidade'
    )


class NeighborhoodList(Schema):
    """Listagem básica de bairros."""
    id: int = Field(..., description='ID do bairro')
    name: str = Field(..., description='Nome do bairro')
    city_name: str = Field(
        ...,
        alias='city.name',
        description='Nome da cidade'
    )


class NeighborhoodInPost(ModelSchema):
    """Entrada para criação de bairro."""

    city_id: int = Field(..., description='ID da cidade')

    class Meta:
        model = Neighbordhood
        exclude = ['id', 'city']


class NeighborhoodInPut(ModelSchema):
    """Entrada para edição de bairro."""

    city_id: int = Field(..., description='ID da cidade')

    class Meta:
        model = Neighbordhood
        exclude = ['id', 'city']


class NeighborhoodOut(ModelSchema):
    """Saída completa de bairro."""
    city: CityList = Field(..., description='Cidade')

    class Meta:
        model = Neighbordhood
        fields = "__all__"


class AddressInPost(ModelSchema):
    """Schema de entrada para criação de endereço."""
    
    neighborhood_id: int = Field(
        ...,
        description='ID do bairro'
    )

    class Meta:
        model = Address
        exclude = [
            'id',
            'neighbordhood'
        ]


class AddressInPut(ModelSchema):
    """Schema de entrada para edição de endereço."""

    neighborhood_id: int = Field(
        ...,
        description='ID do bairro'
    )

    class Meta:
        model = Address
        exclude = [
            'id',
            'neighbordhood'
        ]


class AddressList(Schema):
    """Listagem de endereço."""
    id: int = Field(..., description='ID do endereço')
    street: str = Field(..., description='Rua')
    number: str = Field(..., description='Número')
    neighborhood_name: str = Field(
        ...,
        alias='neighbordhood.name',
        description='Nome do bairro'
    )
    city_name: str = Field(
        ...,
        alias='neighbordhood.city.name',
        description='Cidade'
    )
    federative_unit_acronym: str = Field(
        ...,
        alias='neighbordhood.city.federative_unit.acronym',
        description='UF'
    )

class AddressFilter(FilterSchema):

    id: Optional[int] = Field(
        None,
        q='id__exact',
        description='ID do endereço'
    )
    neighbordhood_id: Optional[int] = Field(
        None,
        q='neighbordhood__id__exact',
        description='ID do bairro'
    )
    city_id: Optional[int] = Field(
        None,
        q='neighbordhood__city__id__exact',
        description='ID da cidade'
    )
    federative_unit_id: Optional[int] = Field(
        None,
        q='neighbordhood__city__federative_unit__id__exact',
        description='ID da UF'
    )

class AddressOut(ModelSchema):
    """Saída completa de endereço."""
    neighbordhood: NeighborhoodOut = Field(..., description='Bairro')

    class Meta:
        model = Address
        fields = "__all__"
