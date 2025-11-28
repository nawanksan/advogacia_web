from internal_api.modules.core.users.models import CustomUsers
from ninja import Field, Schema, FilterSchema, ModelSchema

class UserFilter(FilterSchema):
    username_id: int = Field(
        None,
        q='id__exact',
        description='ID do usuário'
    )
    username: str = Field(
        None,
        q='username__istartswith',
        description='Nome do usuário'
    )
    is_active: bool = Field(
        None,
        q='is_active',
        description='Está ativo?')
    
class UsersList(ModelSchema):

    employee_name: str = Field(
        None,
        alias='employee.full_name',
        description="Nome completo do usuario"
    )

    class Meta:
        model = CustomUsers
        fields = ['id', 'username', 'is_active']

class UserstOutSchema(Schema):
    id: int = Field(
        ...,
        description="ID do usuario"
    )
    username: str = Field(
        ...,
        description="Usarname"
    )


class UsersInPostSchema(ModelSchema):
    full_name: str = Field(
        ...,
        description="nome completo do usuario"
    )

    class Meta:
        model = CustomUsers
        fields = "__all__"
    