from ninja_extra import status
from django.db import models, transaction
from typing import Any, Dict, Tuple, Union
from internal_api.modules.core.utils.classes import Service
from internal_api.modules.employee.repositories import EmployeeRepository
from internal_api.modules.core.users.services import UserService


class EmployeeService(Service):
    """
    Camada responsável pelas regras de negócio
    """

    repository = EmployeeRepository
    
    # @classmethod
    # def validate_payload(cls, *, payload, id = None, **kwargs):
    
    @classmethod
    def post(
        cls,
        *,
        payload: Dict[str, Any],
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Método responsável por criar um funcionário.
        """
        
        try:
            with transaction.atomic():
                status_code: int
                message_or_object: str
                
                # request = kwargs.get('request', None)
                
                status_code, message_or_object = cls.validate_payload(
                    payload=payload
                )
                
                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return message
                
                username = payload.pop('username')
                password = payload.pop('password')
                
                instance = EmployeeRepository.post(
                    payload=payload
                )
                
                if username != '':
                    status_code, message_or_object = UserService.post(
                        employee=instance,
                        payload={'usename': username, 'password': password}
                    )
                    
                    if status_code != status.HTTP_200_OK:
                        message = message_or_object
                        return message
                    
                return status.HTTP_201_CREATED, instance
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': f'Error! {str(error)}'
            }