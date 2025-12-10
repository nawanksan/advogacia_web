from datetime import date
from typing import Optional
from ninja import Field, FilterSchema, ModelSchema, Schema
from internal_api.modules.address.schemas import AddressInPost, AddressInPut, AddressOut
from internal_api.modules.employee.models import Employee, Role

class RoleFilter(FilterSchema):
    """
    Schema responsável por mostrar os campos de filtragem de cargos.
    """

    role_id: int = Field(None, q='id__exact', description='ID do cargo')
    name: str = Field(None, q='name__istartswith', description='Descrição')
    # no_permissions_linked: bool = Field(
    #     None,
    #     q='rolepermission_role_role__isnull',
    #     description='Não possui permissões vinculadas?',
    # )
    is_active: bool = Field(None, q='is_active', description='Está ativo?')


class RoleList(Schema):
    """
    Schema responsável por mostrar os campos de listagem de cargos.
        - id: ID do cargo;
        - description: Descrição;
        - is_active: Está ativo?
    """

    id: int = Field(..., description='ID do cargo')
    name: str = Field(..., description='Descrição')
    description: str = Field(..., description='Descrição')
    is_active: bool = Field(..., description='Está ativo?')


class RoleInPost(ModelSchema):
    """
    Schema responsável por armazenar os campos de entrada de cargos.
        - description: Descrição;
    """

    class Meta:  # pylint: disable=missing-class-docstring
        model = Role
        exclude = [
            'id',
            'is_active',
            'last_modification',
            'registration'
        ]


class RoleInPut(ModelSchema):
    """
    Schema responsável por armazenar os campos de edição de cargos.
        - description: Descrição;
    """

    class Meta:  # pylint: disable=missing-class-docstring
        model = Role
        exclude = [
            'id',
            'is_active',
            'last_modification',
            'registration'
        ]


class RoleOut(ModelSchema):
    """
    Schema responsável por mostrar os campos de saída de cargos.
        - id: ID do cargo;
        - description: Descrição;
        - is_active: Está ativo?
    """

    class Meta:  # pylint: disable=missing-class-docstring
        model = Role
        exclude = [
            'last_modification',
            'registration'
        ]
        
class RoleGetIdName(Schema):
    id: int = Field(..., description='ID do cargo')
    name: str = Field(..., description='Nome do cargo')
    


class EmployeeList(Schema):
    id: int = Field(
        ...,
        description='ID do funcionario'
    )
    full_name: str = Field(
        ...,
        description='Nome completo'
    )
    role_name: str = Field(
        ...,
        alias='role.name',
        description='Descrição do cargo'
    )
    is_active: bool = Field(
        ...,
        description='Está ativo?'
    )

class EmployeeFilter(FilterSchema):
    employee_id: int = Field(
        None,
        q='id__exact',
    )
    full_name: str = Field(
        None,
        q='full_name__istartswith',
        description='Nome completo'
    )
    role: str = Field(
        None,
        q='role__name__istartswith',
        description='Descrição do cargo',
    )
    is_active: bool = Field(
        None,
        q='is_active',
        description='Está ativo?',
    )

class EmployeeOutSchema(ModelSchema):
    
    address: Optional[AddressOut] = Field(..., description='Endereço')
    role: Optional[RoleGetIdName] = Field(..., description='Cargo')
    username: Optional[str] = Field(None, description='Nome de usuário')
    

    @staticmethod
    def resolve_username(obj):
        if hasattr(obj, 'user_employee_employee'):
            return obj.user_employee_employee.username
        return None

    class Meta:
        model = Employee
        exclude = [
            'last_modification',
            'registration',
        ]

class EmployeeInPost(ModelSchema):
    username: Optional[str] = Field(None, description='Nome de usuário')
    role_id: int = Field(..., description='ID do cargo')
    oab: Optional[str] = Field(
        None,
        description='OAB do advogado'
    )
    oab_status: Optional[str] = Field(
        None,
        description='Status do OAB do advogado'
    )
    specialty: Optional[str] = Field(
        None,
        description='Especialidade do advogado'
    )
    cellphone: Optional[str] = Field(
        None,
        description="Numero de celular"
    )
    address: AddressInPost = Field(
        ...,
        description='Endereço'
    )
    is_system_user: Optional[bool] = Field(
        None,
        description='funcionario vai usar o sistema?'
    )

    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            'is_active',
            'last_modification',
            'registration'
        ]

class EmployeeInPut(ModelSchema):
    username: Optional[str] = Field(None, description='Nome de usuário')
    # password: Optional[str] = Field(None, description='senha do sistema')
    role_id: int = Field(..., description='ID do cargo')
    address: Optional[AddressInPut] = Field(
        ...,
        description='Endereço'
    )
    is_system_user: Optional[bool] = Field(
        None,
        description='funcionario vai usar o sistema?'
    )
    
    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            'is_active',
            'last_modification',
            'registration'
        ]