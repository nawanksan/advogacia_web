from datetime import date
from typing import Optional
from ninja import Field, FilterSchema, ModelSchema, Schema
from internal_api.modules.address.schemas import AddressInPost
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
        fields = '__all__'


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

class EmployeeOutSchema(Schema):
    id: int = Field(
        ...,
        description='ID do funcionário'
    )
    full_name: str = Field(
        ...,
        description='Nome completo'
    )
    cpf: str = Field(
        ...,
        description='CPF'
    )
    email: str = Field(
        ...,
        description='Email'
    )
    birth_date: date = Field(
        ...,
        description='Data de aniversário'
    )
    oab: str = Field(
        None,
        description='OAB do advogado'
    )
    oab_status: str = Field(
        None,
        description='Status do OAB'
    )
    type: str = Field(
        ...,
        description=('tipo de usuario')
    )
    specialty: str = Field(
        None,
        description='Status do OAB'
    )
    is_active: bool = Field(
        ...,
        description='Está ativo?'
    )

class EmployeeInPost(ModelSchema):
    username: str = Field(None, description='Nome de usuário')
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
    address: AddressInPost = Field(
        ...,
        description='Endereço'
    )

    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            'oab_status',
            'oab',
            'specialty',
            'is_active'
        ]

class EmployeeInPut(ModelSchema):
    username: Optional[str] = Field(None, description='Nome de usuário')
    password: Optional[str] = Field(None, description='senha do sistema')
    role_id: int = Field(..., description='ID do cargo')
    # address_id: AddressInPost = Field(
    #     ...,
    #     description='Endereço'
    # )
    
    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            # 'address'
            'is_active'
        ]