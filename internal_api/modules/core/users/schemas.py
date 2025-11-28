from ninja import Field, Schema

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
    