from typing import Optional
from ninja import NinjaAPI, Schema
from ninja_extra import api_controller
# from internal_api.core.users.auth import CustomJWTAuth
from pydantic import Field

class UserLoginBase(Schema):
    full_name: Optional[str] = Field(
        None,
        description='Nome completo'
    )
    employee_id: Optional[int] = Field(
        None,
        description='ID do funcionario'
    )

class CustomTokenObtainOutSchema(Schema):
    """
    Schema responsável por tratar o Schema (modelo Pydantic) de resposta para o login
    com o token de acesso.
    """

    access: str
    refresh: str
    user: UserLoginBase = Field(..., description='Usuário')

class CustomTokenObtainSchema(Schema):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Senha")
    # user: UserLoginBase