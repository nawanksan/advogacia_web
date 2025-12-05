"""
Local onde registra os controllers da aplicação interna
para a implementação das rotas dos end-points.
"""
from internal_api.modules.address.controllers import AddressController, CityController, CountryController, FederativeUnitController, NeighborhoodController
from internal_api.modules.employee.controllers import EmployeeController, RoleController
from ninja import Swagger
from internal_api.modules.core.token.controllers import TokenJWTControllers
from ninja_extra import NinjaExtraAPI
from internal_api.modules.core.main.auth import CustomJWTAuth, JWTAuth
from internal_api.modules.core.users.controllers import UserController
from django.contrib.admin.views.decorators import  staff_member_required


internal_api = NinjaExtraAPI(
    auth=CustomJWTAuth(),
    title="Meu sistema Jurídico API",
    version="0.0.1",
    docs_decorator=staff_member_required,
    description="API para gerenciamento de casos, usuarios",
    docs=Swagger(
        settings={
            "persistAuthorization": True,
            "Filter": True,
            "docExpansion": "none",
        }
    )
)

# Módulo CORE
internal_api.register_controllers(
    TokenJWTControllers,
    UserController
)

# Módulo ADDRESS
internal_api.register_controllers(
    CountryController,
    FederativeUnitController,
    CityController,
    NeighborhoodController,
    AddressController,
)

# Módulo EMPLOYEE
internal_api.register_controllers(
    EmployeeController,
    RoleController
)

# # Módulo CASE
# internal_api.register_controllers(
#     CaseController,
# )