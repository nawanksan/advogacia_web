from ninja import NinjaAPI, Schema
from ninja_extra import api_controller
# from internal_api.core.users.auth import CustomJWTAuth
from pydantic import Field

class UserLoginBase(Schema):
    id: int
    username: str
    email: str

class CustomTokenObtainOutSchema(Schema):
    """
    Schema responsável por tratar o Schema (modelo Pydantic) de resposta para o login
    com o token de acesso.
    """

    token: str = Field(..., description='Token de acesso')
    user: UserLoginBase = Field(..., description='Usuário')

class CustomTokenObtainSchema(Schema):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Senha")