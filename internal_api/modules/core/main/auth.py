from ninja_extra import api_controller
from ninja_jwt.authentication import JWTAuth
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError
# from ninja_jwt.controller import NinjaJWTDefaultController

class  JWTAuth(JWTAuth):
    
    # def __init__(self, expected_audience: str, type_user: str):
    #     self.expected_audience = expected_audience
    #     self.type_user = type_user
    #     super().__init__()

    def authenticate(self, request, token):
        """
        Autentica o usuário usando seu modelo CustomUsers.
        """
        try:
            # validated_token = self.get_validated_token(token)
            # valida o token e pega o usuário
            user = super().authenticate(request, token)

            if not user:
                raise HttpError(401, _("Invalid token or user does not exist"))
            # opcional: validar audience dentro do token
            # if self.expected_audience:
            #     if token.payload.get("aud") != self.expected_audience:
            #         raise HttpError(403, _("Invalid audience"))
            # if validated_token.get('aud') != self.expected_audience and not user.is_superuser:
            #     raise HttpError(401, _('Invalid token for this API'))
            # if user.type_user != self.type_user and not user.is_superuser:
            #     raise HttpError(403, _("User does not have access to this API"))

            return user
        except Exception:
            raise HttpError(401, _("Invalid token"))
        