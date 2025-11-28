from ninja import Field, Schema, FilterSchema

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

class UserstOutSchema(Schema):
    id: int = Field(
        ...,
        description="ID do usuario"
    )
    full_name: str = Field(
        ...,
        description="nome completo do usuario"
    )


class UsersInPostSchema(Schema):
    full_name: str = Field(
        ...,
        description="nome completo do usuario"
    )
    