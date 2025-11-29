from ninja import Field, FilterSchema, ModelSchema, Schema

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