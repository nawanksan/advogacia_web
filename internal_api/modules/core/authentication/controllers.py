from ninja_extra import api_controller
from ninja_jwt.controller import NinjaJWTDefaultController


@api_controller(
    "/auth",
    tags=["CORE - AUTH"]
)
class AuthController(NinjaJWTDefaultController):
    pass