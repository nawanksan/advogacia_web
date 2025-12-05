from typing import Any, Dict, Optional, Tuple, Union
from django.db import models, transaction, IntegrityError
from django.db.models import ObjectDoesNotExist
from ninja_extra import status

from internal_api.modules.core.utils.remove_excess_spaces import remove_excess_spaces
from internal_api.modules.core.utils.classes import Service
from internal_api.modules.address.repositories import (
    CountryRepository,
    FederativeUnitRepository,
    CityRepository,
    NeighborhoodRepository,
    AddressRepository,
)

class CountryServices(Service):
    
    repository = CountryRepository

    @classmethod
    def validate_payload(  # noqa: PLR0911, PLR0912
        cls,
        *,
        payload: Dict[str, Any],
        id: Optional[int] = None,
        **kwargs,
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        """
        Método responsável por implementar as regras
        de negócio do submódulo de país.
        """
        status_code: int
        message: Dict
        country: Optional[models.Model] = None
        django_admin: Optional[bool] = kwargs.get('django_admin', False)

        get_name: str = remove_excess_spaces(payload.get('name', '')).upper()
        if get_name == '':  # noqa: PLC1901
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Nome do país não pode ser vazio.'
            }

        get_abbreviation: str = remove_excess_spaces(
            payload.get('abbreviation', '')
        ).upper()
        if get_abbreviation == '':  # noqa: PLC1901
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Sigla do país não pode ser vazia.'
            }

        if (
            len(get_abbreviation.strip()) != 3  # noqa: PLR2004
            or not get_abbreviation.isalpha()
        ):
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Sigla deve possuir exatamente três letras.'
            }

        country_list = cls.list()
        country_filter_name = country_list.filter(
            name=get_name, is_active=True
        )
        country_filter_abbreviation = country_list.filter(
            abbreviation=get_abbreviation, is_active=True
        )
        if id is not None:
            status_code, country_or_message = cls.get(id=id)
            if status_code != status.HTTP_200_OK:
                message = country_or_message
                return status_code, message

            country: Any = country_or_message

            if not country.is_active and not django_admin:
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'País inativo, não é possível '
                        'modificar suas informações.'
                    )
                }

            if country_filter_name.exclude(id=id).exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': 'Já existe este país.'
                }

            if country_filter_abbreviation.exclude(id=id).exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': 'Já existe esta sigla.'
                }

        else:
            if country_filter_name.exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': 'Já existe este país.'
                }

            if country_filter_abbreviation.exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': 'Já existe esta sigla.'
                }

        return status.HTTP_200_OK, country

class FederativeUnitService(Service):

    repository = FederativeUnitRepository

    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:

        name = remove_excess_spaces(payload.get("name", "")).upper()
        abbreviation = remove_excess_spaces(payload.get("abbreviation", "")).upper()
        country_id = payload.get("country_id")

        if name == "":
            return status.HTTP_400_BAD_REQUEST, {"message": "Nome não pode ser vazio."}

        if abbreviation == "":
            return status.HTTP_400_BAD_REQUEST, {"message": "Sigla não pode ser vazia."}

        # FK obrigatória
        from internal_api.modules.address.models import Country

        if not Country.objects.filter(id=country_id, is_active=True).exists():
            return status.HTTP_400_BAD_REQUEST, {"message": "País informado é inválido."}

        # Verificar duplicidade
        qs = cls.list().filter(name=name, abbreviation=abbreviation, country_id=country_id)
        if id is not None:
            qs = qs.exclude(id=id)
        if qs.exists():
            return status.HTTP_400_BAD_REQUEST, {
                "message": "Já existe uma UF com esse nome e sigla."
            }

        return status.HTTP_200_OK, None

    @classmethod
    def post(
        cls, *, payload: Dict[str, Any]
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:

        try:
            with transaction.atomic():

                status_code, msg = cls.validate_payload(payload=payload)
                if status_code != status.HTTP_200_OK:
                    return status_code, msg

                instance = cls.repository.post(
                    payload=payload,
                )
                return status.HTTP_201_CREATED, instance

        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}

    # -------------------------------
    # PUT
    # -------------------------------
    @classmethod
    def put(
        cls, *, id: int, payload: Dict[str, Any]
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:

        try:
            with transaction.atomic():

                status_code, instance = cls.get(id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, instance

                status_code, msg = cls.validate_payload(payload=payload, id=id)
                if status_code != status.HTTP_200_OK:
                    return status_code, msg

                updated = cls.repository.put(
                    instance=instance,
                    payload=payload,
                )
                return status.HTTP_200_OK, updated

        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}


class CityService(Service):

    repository = CityRepository

    @classmethod
    def validate_payload(cls, *, payload: Dict[str, Any], id: Optional[int] = None):

        name = remove_excess_spaces(payload.get("name", "")).upper()
        federative_unit_id = payload.get("federative_unit_id")

        if name == "":
            return status.HTTP_400_BAD_REQUEST, {"message": "Nome não pode ser vazio."}

        # FK obrigatória
        from internal_api.modules.address.models import FederativeUnit
        if not FederativeUnit.objects.filter(id=federative_unit_id, is_active=True).exists():
            return status.HTTP_400_BAD_REQUEST, {"message": "UF informada é inválida."}

        qs = cls.list().filter(name=name, federative_unit_id=federative_unit_id)
        if id:
            qs = qs.exclude(id=id)
        if qs.exists():
            return status.HTTP_400_BAD_REQUEST, {"message": "Cidade já cadastrada nessa UF."}

        return status.HTTP_200_OK, None


    @classmethod
    def post(cls, *, payload: Dict[str, Any]):
        try:
            with transaction.atomic():
                st, msg = cls.validate_payload(payload=payload)
                if st != status.HTTP_200_OK:
                    return st, msg

                instance = cls.repository.post(payload=payload)
                return status.HTTP_201_CREATED, instance
        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}

    @classmethod
    def put(cls, *, id: int, payload: Dict[str, Any]):
        try:
            with transaction.atomic():
                st, instance = cls.get(id=id)
                if st != status.HTTP_200_OK:
                    return st, instance

                st, msg = cls.validate_payload(payload=payload, id=id)
                if st != status.HTTP_200_OK:
                    return st, msg

                updated = cls.repository.put(
                    instance=instance,
                    payload=payload
                )
                return status.HTTP_200_OK, updated
        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}


class NeighborhoodService(Service):

    repository = NeighborhoodRepository

    @classmethod
    def validate_payload(cls, *, payload: Dict[str, Any], id: Optional[int] = None):

        name = remove_excess_spaces(payload.get("name", "")).upper()
        city_id = payload.get("city_id")

        if name == "":
            return status.HTTP_400_BAD_REQUEST, {"message": "Nome não pode ser vazio."}

        from internal_api.modules.address.models import City
        if not City.objects.filter(id=city_id, is_active=True).exists():
            return status.HTTP_400_BAD_REQUEST, {"message": "Cidade informada é inválida."}

        qs = cls.list().filter(name=name, city_id=city_id)
        if id:
            qs = qs.exclude(id=id)
        if qs.exists():
            return status.HTTP_400_BAD_REQUEST, {
                "message": "Bairro já cadastrado nessa cidade."
            }

        return status.HTTP_200_OK, None


    @classmethod
    def post(cls, *, payload: Dict[str, Any]):
        try:
            with transaction.atomic():
                st, msg = cls.validate_payload(payload=payload)
                if st != status.HTTP_200_OK:
                    return st, msg

                instance = cls.repository.post(payload=payload)
                return status.HTTP_201_CREATED, instance
        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}

    @classmethod
    def put(cls, *, id: int, payload: Dict[str, Any]):
        try:
            with transaction.atomic():
                st, instance = cls.get(id=id)
                if st != status.HTTP_200_OK:
                    return st, instance

                st, msg = cls.validate_payload(payload=payload, id=id)
                if st != status.HTTP_200_OK:
                    return st, msg

                updated = cls.repository.put(
                    instance=instance,
                    payload=payload
                )
                return status.HTTP_200_OK, updated

        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}


class AddressService(Service):

    repository = AddressRepository

    @classmethod
    def validate_payload(cls, *, payload: Dict[str, Any], id: Optional[int] = None):

        street_name = remove_excess_spaces(payload.get("street_name", "")).upper()
        number = payload.get("number")
        postal_code = remove_excess_spaces(payload.get("postal_code", ""))
        neighbordhood_id = payload.get("neighbordhood_id")

        if street_name == "":
            return status.HTTP_400_BAD_REQUEST, {
                "message": "Nome da rua não pode ser vazio."
            }

        if not number:
            return status.HTTP_400_BAD_REQUEST, {
                "message": "Número é obrigatório."
            }

        if postal_code == "":
            return status.HTTP_400_BAD_REQUEST, {
                "message": "CEP é obrigatório."
            }

        from internal_api.modules.address.models import Neighbordhood
        if not Neighbordhood.objects.filter(id=neighbordhood_id, is_active=True).exists():
            return status.HTTP_400_BAD_REQUEST, {
                "message": "Bairro informado é inválido."
            }

        return status.HTTP_200_OK, None


    @classmethod
    def post(cls, *, payload: Dict[str, Any]):
        try:
            with transaction.atomic():

                st, msg = cls.validate_payload(payload=payload)
                if st != status.HTTP_200_OK:
                    return st, msg

                instance = cls.repository.post(
                    payload=payload
                )
                return status.HTTP_201_CREATED, instance

        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                "message": str(e)
            }

    @classmethod
    def put(cls, *, id: int, payload: Dict[str, Any]):
        try:
            with transaction.atomic():

                st, instance = cls.get(id=id)
                if st != status.HTTP_200_OK:
                    return st, instance

                st, msg = cls.validate_payload(payload=payload, id=id)
                if st != status.HTTP_200_OK:
                    return st, msg

                updated = cls.repository.put(
                    instance=instance,
                    payload=payload
                )
                return status.HTTP_200_OK, updated

        except IntegrityError as e:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": str(e)}
