from ninja_extra import status
from django.db import IntegrityError, models, transaction
from typing import Any, Dict, Optional, Tuple, Union
from internal_api.modules.address.services import AddressService
from internal_api.modules.core.utils.classes import Service
from internal_api.modules.employee.repositories import EmployeeRepository
from internal_api.modules.core.users.services import UserService
from internal_api.modules.core.utils.remove_excess_spaces import remove_excess_spaces


class EmployeeService(Service):
    """
    Camada responsável pelas regras de negócio
    """

    repository = EmployeeRepository
    
    @classmethod
    def validate_payload(
        cls,
        *,
        payload: Dict[str, Any],
        id: Optional[int] = None, 
        **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        status_code: int
        message: Dict
        employee: Optional[models.Model]
        full_name: str = remove_excess_spaces(
            payload.get('full_name', '')
        )
        cpf: str = remove_excess_spaces(
            payload.get('cpf')
        )
        email: str = remove_excess_spaces(
            payload.get('email', '')
        )
        birth_date: str = payload.get('birth_date', '')
        cellphone: str = payload.get('cellphone', '')
        oab: Optional[str] = payload.get('oab', '')
        oab_status: Optional[str] = payload.get('oab_status', '')
        specialty: Optional[str] = payload.get('specialty', '')
        
        # status_code, role_or_message = RoleService.get(
        #     id=payload.get('role_id', None)
        # )
        # if status_code != status.HTTP_200_OK:
        #     message = role_or_message
        #     return status_code, message

        # role: Any = role_or_message
        filter_by_cpf: Any = cls.list().filter(cpf=cpf, is_active=True)
        filter_by_email: Any = cls.list().filter(email=email, is_active=True)
        
        if id is not None:
            status_code, employee_or_message = cls.get(id=id)
            if status_code != status.HTTP_200_OK:
                message = employee_or_message
                return message
            
            employee: Any = employee_or_message

            if not employee.is_active:
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'Funcionário inativo, '
                        'não é possível mudar suas informações'
                    )
                }

                
            if filter_by_cpf.exclude(id=id).exict():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'Já existe um cadastro com o CPF informado'
                    )
                }

            if filter_by_email.exclude(id=id).exict():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'Já existe um cadastro com o e-mail informado'
                    )
                }
                
        else:
            if filter_by_cpf.exclude(id=id).exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'CPF já cadastrado'
                    )
                }

            if filter_by_email.exclude(id=id).exists():
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'Já existe um cadastro com o e-mail informado'
                    )
                }

        if not full_name:
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Informa a data de aniversário'
            } 
        
        if not birth_date:
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Informa a data de aniversário'
            }
            
        if not email:
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Informa o email de aniversário'
            }
        
        if cellphone > 11:
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'O número de contato'
                ' deve ter no máximo 11 caracteres'
            }
        
        # if oab_status == in ['IN', 'SU']:
        #     return status.HTTP_400_BAD_REQUEST, {
        #         'message': 'o OAB inválido'
        #     }
            
    
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
                address_payload: Dict = payload.pop('address', {})

                # request = kwargs.get('request', None)

                status_code, message_or_object = cls.validate_payload(
                    payload=payload
                )

                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return message
                
                status_code, message_or_object = AddressService.validate_payload(
                    payload=address_payload
                )

                status_code, message_or_object = AddressService.post(
                    payload=address_payload
                )

                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return message

                username = remove_excess_spaces(
                    payload.get('username')
                )
                password = remove_excess_spaces(
                    payload.get('password')
                )

                # if not username:
                #     return status.HTTP_400_BAD_REQUEST, {
                #         'message': (
                #             'O nome de usuário é obrigatório'
                #         )
                #     }
                
                # if username and username > 60:
                #     return status.HTTP_400_BAD_REQUEST, {
                #         'message': (
                #             'O nome de usuário é obrigatório'
                #         )
                #     }
                
                # if not password:
                #     return status.HTTP_400_BAD_REQUEST, {
                #         'message': (
                #             'A senha é obrigatória'
                #         )
                #     }

                instance = EmployeeRepository.post(
                    payload=payload
                )

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

    @classmethod
    def put(
        cls,
        *,
        payload: Dict[str, Any],
        **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
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
                
        instance = EmployeeRepository.put(
            payload=payload
        )
                
        if username != '':
            status_code, message_or_object = UserService.put(
                employee=instance,
                payload={'usename': username, 'password': password}
            )

            if status_code != status.HTTP_200_OK:
                message = message_or_object
                return message
                    
        return status.HTTP_200_OK, instance