from typing import Any, Dict, List, Optional, Tuple, Union
from django.db import models, transaction
from django.http import Http404
from ninja_extra import status
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldError
from django.utils.translation import gettext_lazy as _
# from .omitted_fields import omitted_fields

class Repository:

    model: models.Model
    
    @classmethod
    def update_payload(
        cls,*,payload: Dict, **kwargs
    ) -> Dict:
        updated_payload: Dict ={
            **payload
        }
        return updated_payload

    @classmethod
    def list(cls) -> models.QuerySet:
        """
        Lista todos os registros.
        """
        return cls.model.objects.all()
        

    @classmethod
    def get(cls, *, id: int, only: Optional[List[str]] = None) -> models.Model:
        """
        Obtém um registro.
        """

        if only:
            valid_fields = {field.name for field in cls.model._meta.get_fields()}
            invalid_fields = set(only) - valid_fields
            if invalid_fields:
                message: str = _("Invalid fields")
                raise FieldError(f"{message}: {', '.join(invalid_fields)}")
        queryset: models.QuerySet = cls.model.objects.only(*only) if only else cls.model.objects.all()
        return get_object_or_404(queryset, id=id)
    
    @classmethod
    def post(
        cls, *, payload: Dict, **kwargs
    ) -> models.Model:
        """
        Cria um registro.
        """
        payload = cls.update_payload(
            payload=payload, **kwargs
        )
        return cls.model.objects.create(**payload)
    
    @classmethod
    def put(
        cls,
        *,
        instance: models.Model,
        payload: Dict,
        **kwargs,
    ) -> models.Model:
        """
        Atualiza um registro.
        """
        if not isinstance(instance, cls.model):
            raise Http404(
                "The instance does not belong to the model."
                f"{cls.model._meta.verbose_name}."
            )

        payload = cls.update_payload(
            instance=instance,
            payload=payload,
            **kwargs,
        )
        for key, value in payload.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class Service:

    repository: Repository

    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None, **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        instance: Optional[models.Model] = None
        return status.HTTP_200_OK, instance

    @classmethod
    def list(cls,*,filters: Optional[Any] = None) -> models.QuerySet:
        queryset = cls.repository.list()
        if filters:
            queryset =filters.filter(queryset)
        return queryset
    
    @classmethod
    def get(cls,*,id: int, only: Optional[List[str]] = None) -> Tuple[int, models.Model | Dict[str, str]]:
        try:
            return status.HTTP_200_OK, cls.repository.get(id=id, only=only)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': (
                    f'{cls.repository.model._meta.verbose_name.capitalize()}'
                )
            }
        
    @classmethod
    def post(
        cls,*,payload: Dict[str, Any], **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str,str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                status_code, message = cls.validate_payload(payload=payload)
                if status_code != status.HTTP_200_OK:
                    return status_code, message

                instance = cls.repository.post(
                    payload=payload
                )
                return status.HTTP_201_CREATED, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': str(error)
            }
        
    @classmethod
    def put(
        cls, *, id: int, payload: Dict[str, Any], **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                status_code, message_or_object = cls.validate_payload(
                    payload=payload, id=id
                )
                if status_code != status.HTTP_200_OK:
                    message: Dict = message_or_object
                    return status_code, message

                instance: models.Model = message_or_object

                instance = cls.repository.put(
                    instance=instance,
                    payload=payload,
                )
                return status.HTTP_201_CREATED, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': str(error)
            }


class Controller:
    """
    Responsável por lidar com a comunicação entre a camada de apresentação
    e a camada de serviço.
    """

    service: Service