from ninja_extra import status
from django.db import IntegrityError, models, transaction
from typing import Any, Dict, Optional, Tuple, Union
from internal_api.modules.address.repositories import AddressRepository
from internal_api.modules.address.services import AddressService
from internal_api.modules.core.users.repositories import UserRepository
from internal_api.modules.core.utils.classes import Service
from internal_api.modules.employee.repositories import EmployeeRepository, RoleRepository
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
        return status.HTTP_200_OK, employee
    
    # @classmethod
    # def list(cls, *, filters: Optional[Any] = None):
    #     queryset = super().list(filters=filters)

    #     return {
    #         "count": queryset.count(),
    #         "results": list(queryset)
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
                
                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return status_code, message

                status_code, message_or_object = AddressService.post(
                    payload=address_payload
                )

                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return status_code, message
                
                post_address: Any = message_or_object

                username: str = payload.pop('username')
                is_system_user: bool = payload.get('is_system_user', False)

                payload['address_id'] = post_address.id
                instance = EmployeeRepository.post(
                    payload=payload
                )

                if is_system_user and username != '':
                    status_code, message_or_object = UserService.post(
                        employee=instance,
                        payload={'usename': username}
                    )
                    
                    post_username: Any = message_or_object
                    
                    instance.username = post_username

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
        try:
            with transaction.atomic():
                status_code: int
                message: str
                address_payload: Dict = payload.pop('address', {})


                # request = kwargs.get('request', None)

                status_code, message_or_object = cls.validate_payload(
                    payload=payload
                )

                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return message

                # is_sistem_user: bool = payload.get('is_sistem_user', False)
                employee: Any = message_or_object

                status_code, message_or_object = AddressService.validate_payload(
                    id=employee.address.id,
                    payload=address_payload
                )

                if status_code != status.HTTP_200_OK:
                    message = message_or_object
                    return message

                address: models.Model = message_or_object

                AddressRepository.put(
                    instance=address,
                    payload=address_payload
                )

                username: str = payload.pop('username', '')
                is_system_user: bool = payload.get('is_system_user', False)
                
                
                instance = EmployeeRepository.put(
                    instance=employee,
                    payload=payload
                )

                has_previous_user: bool = hasattr(
                    instance, 'user_employee_employee'
                )

                if has_previous_user:
                    UserRepository.put(
                        instance=instance.user_employee_employee
                    )
                elif is_system_user and username != '':
                    status_code, message_or_object = UserService.post(
                        employee=instance,
                        payload={'usename': username}
                    )

                    if status_code != status.HTTP_200_OK:
                        message = message_or_object
                        return message

                    post_user: Any = message_or_object
                    
                    instance.username = post_user.username

                return status.HTTP_200_OK, instance
            
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': f'Error! {str(error)}'
            }
            
class RoleService(Service):
    """
    Responsável por implementar os serviços
    relacionados aos cargos de funcionários,
    utilizados para realizar operações
    sobre regras de negócio, antes de persistir
    os dados na camada de armazenamento.
    As regras de negócio implementadas foram:
        - Não permitir que o cargo seja vazio;
        - Não permitir editar as informações de um cargo inativo;
        - Verificar se há funcionários vinculados ao cargo;
    """

    repository = RoleRepository
    
    @classmethod
    def list_queryset(cls, *, filters: Optional[Any] = None):
        return super().list(filters=filters)

    @classmethod
    def validate_payload(
        cls, *, payload: Dict[str, Any], id: Optional[int] = None, **kwargs
    ) -> Tuple[int, Optional[models.Model | Dict[str, str]]]:
        """
        Método responsável por validar os dados do cargo.
        """
        role: Optional[models.Model] = None
        # django_admin: bool = kwargs.get('django_admin', False)

        name = remove_excess_spaces(payload.get('name', '')).upper()
        if name == '':  # noqa: PLC1901
            return status.HTTP_400_BAD_REQUEST, {
                'message': 'Cargo não pode ser vazio.'
            }

        filter_name: Any = cls.list_queryset().filter(name=name, is_active=True)
        if id is not None:
            status_code, role_or_message = cls.get(id=id)
            if status_code != status.HTTP_200_OK:
                message = role_or_message
                return status_code, message

            role: Any = role_or_message

            if not role.is_active:
                return status.HTTP_400_BAD_REQUEST, {
                    'message': (
                        'Cargo inativo, não é possível '
                        'modificar suas informações.'
                    )
                }

            if filter_name.exists() and name != role.name:
                return status.HTTP_400_BAD_REQUEST, {
                    'message': 'Cargo já existe.'
                }
        elif filter_name.exists():
            return status.HTTP_400_BAD_REQUEST, {'message': 'Cargo já existe.'}
        return status.HTTP_200_OK, role

    # @classmethod
    # def list(cls, *, filters: Optional[Any] = None) -> models.QuerySet:
    #     "Método responsável por listar os cargos de funcionários."
    #     queryset = cls.repository.list()
    #     if filters:
    #         queryset = filters.filter(queryset).distinct()
    #     return queryset
    
    # @classmethod
    # def list(cls, *, filters: Optional[Any] = None):
    #     queryset = super().list(filters=filters)

    #     return {
    #         "count": queryset.count(),
    #         "results": list(queryset)
    #     }

    @classmethod
    def post(
        cls, *, payload: Dict[str, Any], **kwargs
    ) -> Tuple[int, Union[models.Model, Dict[str, str]]]:
        """
        Método responsável por criar um cargo de funcionário.
        """
        try:
            with transaction.atomic():
                status_code: int
                message: Dict[str, str]

                status_code, message_or_object = super().post(
                    payload=payload
                )

                if status_code != status.HTTP_201_CREATED:
                    message: Dict = message_or_object
                    return status_code, message

                instance = message_or_object

                return status.HTTP_201_CREATED, instance
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {
                'message': str(error)
            }