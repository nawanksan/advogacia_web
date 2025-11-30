from datetime import date
from typing import Optional
from ninja import Field, FilterSchema, ModelSchema, Schema
from internal_api.modules.employee.models import Employee

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
    password: str = Field(None, description='senha do sistema')
    role_id: int = Field(..., description='ID do cargo')
    
    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            'is_active'
        ]

class EmployeeInPut(ModelSchema):
    username: Optional[str] = Field(None, description='Nome de usuário')
    password: Optional[str] = Field(None, description='senha do sistema')
    role_id: int = Field(..., description='ID do cargo')
    
    class Meta:
        model = Employee
        exclude = [
            'id',
            'role',
            'is_active'
        ]