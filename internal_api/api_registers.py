"""
Local onde registra os controllers da aplicação interna
para a implementação das rotas dos end-points.
"""
from ninja_extra import NinjaExtraAPI
# from ninja_extra.swagger import Swagger
from ninja_jwt.authentication import JWTAuth

from internal_api.modules.core.users.controllers import UserController
from internal_api.modules.core.authentication.controllers import AuthController


internal_api = NinjaExtraAPI(
    auth=JWTAuth(),
    title="Meu sistema Jurídico API",
    version="0.0.1",
    description="API para gerenciamento de casos, usuarios",
    # docs=Swagger(
    #     settings={
    #         "persistAuthorization": True,
    #         "Filter": True,
    #         "docExpansion": "none",
    #     }
    # )
)

# Módulo CORE
internal_api.register_controllers(
    AuthController,
    UserController
)

# Módulo ADDRESS
# internal_api.register_controllers(
#     AddressController,
# )

# # Módulo CASE
# internal_api.register_controllers(
#     CaseController,
# )