from typing import Dict

from django.db import models
from django.http import Http404

from internal_api.modules.core.utils import remove_excess_spaces
from internal_api.modules.core.utils.classes import Repository
from .models import Address, Country,Neighbordhood, City, FederativeUnit ,AbstractBaseModel

class CountryRepository(Repository):
    """
    Responsável por lidar com a persistência e interação
    com a camada de armazenamento de dados, relacionados ao submódulo de pais.
    """

    model = Country

    # Country
    @classmethod
    def update_payload(
        cls, *, payload: Dict, last_user_id: int, **kwargs
    ) -> Dict:
        """
        Método responsável por atualizar o payload do país.
        """
        updated_payload: Dict = super().update_payload(
            payload=payload, last_user_id=last_user_id
        )
        updated_payload.update({
            'name': remove_excess_spaces(
                updated_payload.get('name', '')
            ).upper(),
            'abbreviation': remove_excess_spaces(updated_payload.get('abbreviation', '').upper()),  # noqa: E501
        })
        return updated_payload


class FederativeUnitRepository(Repository):

    model = FederativeUnit

    @classmethod
    def update_payload(cls, *, payload, **kwargs):

        payload.update(
            {
                'name': remove_excess_spaces(
                    payload.get('name', '')
                ).upper(),
                'abbreviaton': remove_excess_spaces(
                    payload.get('abbreviaton', '')
                ).upper()
            }
        )

        update_payload: Dict = super.update_payload(
            payload=payload
        )

        return update_payload


class CityRepository(Repository):

    model = City

    @classmethod
    def update_payload(cls, *, payload, **kwargs):

        payload.update(
            {
                'name': remove_excess_spaces(
                    payload.get('name', '')
                ).upper()
            }
        )

        update_payload: Dict = super.update_payload(
            payload=payload
        )

        return update_payload


class NeighborhoodRepository(Repository):

    model = Neighbordhood

    @classmethod
    def update_payload(cls, *, payload, **kwargs):

        payload.update(
            {
                'name': remove_excess_spaces(
                    payload.get('name', '')
                ).upper()
            }
        )

        update_payload: Dict = super.update_payload(
            payload=payload
        )

        return update_payload


class AddressRepository(Repository):
    """
    Responsável por lidar com a persistência e interação
    com a camada de armazenamento de dados, relacionados
    ao submódulo de endereço.
    """

    model = Address

    @classmethod
    def update_payload(cls, *, payload, **kwargs):

        payload.update(
            {
                'street_name': remove_excess_spaces(
                    payload.get('street_name', '')
                ).upper(),
                'complements': remove_excess_spaces(
                    payload.get('complements', '')
                ).upper()
            }
        )

        update_payload: Dict = super.update_payload(
            payload=payload
        )

        return update_payload
