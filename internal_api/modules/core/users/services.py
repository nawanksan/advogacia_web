from typing import Any, Dict, Optional, Tuple, Union
from django.db import  models, transaction
from django.db.utils import IntegrityError
from internal_api.modules.core.utils.classes import Service
from internal_api.modules.core.users.repositories import UserRepository
from ninja_extra import status

from internal_api.modules.core.utils.generators import generate_user_password

class UserService(Service):
    
    repository = UserRepository
    
    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None, **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        raise NotImplementedError('Method not implemented.')
    
    @classmethod
    def post(
        cls,
        *,
        payload: Dict[str,Any],
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Método responsável por criar um usuário.
        """
        try:
            with transaction.atomic():
                status_code: int
                message: Dict
                employee = kwargs.get('employee')
                
                password = generate_user_password()
                
                # status_code, message = send_email_username_password(
                #     username=payload.get('username'),
                #     password=password,
                #     email=employee.email,
                #     full_name=employee.full_name,
                # )
                
                # if status_code != status.HTTP_200_OK:
                #     return status_code, message
                
                instance = cls.repository.post(
                    payload={
                        'usernamed':payload.get('username'),
                        'employee_id':employee.id,
                        'password': password
                    }
                )
                return status.HTTP_201_CREATED, instance
                
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': f'Error!: {str(error)}'
            }