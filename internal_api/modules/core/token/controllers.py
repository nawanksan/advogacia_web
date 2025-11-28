# from internal_api.modules.core.main.auth import CustomJWTAuth
from .schemas import CustomTokenObtainOutSchema, CustomTokenObtainSchema, UserLoginBase
from ninja_jwt.controller import ControllerBase
from django.contrib.auth import authenticate
from ninja_extra import api_controller, route
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken

@api_controller(
    'core/',
    tags=['CORE - TOKEN'],
    auth=None
)
class TokenJWTControllers(ControllerBase):
    @route.post(
        'token/',
        response=CustomTokenObtainOutSchema,
        url_name='token_obtain'
    )
    def obtain_token(self, request, user_token: CustomTokenObtainSchema):
        """
        Rota responsável por autenticar o token da requisição e retornar
        informações do usuário para o front-end.
        """
        # autentica usuário usando Django
        user = authenticate(
            request,
            username=user_token.username,
            password=user_token.password
        )

        # ou levante um HTTPException
        if not user:
            raise HttpError(401, "Usuário ou senha inválidos")
        # aqui você pode criar o token JWT usando seu CustomJWTAuth
        refresh = RefreshToken.for_user(user)

        return CustomTokenObtainOutSchema(
            token=str(refresh.access_token),
            user=UserLoginBase(
                id=user.id,
                username=user.username
            )
        )