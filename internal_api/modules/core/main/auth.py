from ninja_extra import api_controller
from ninja_jwt.authentication import JWTAuth
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError
# from ninja_jwt.controller import NinjaJWTDefaultController

class  CustomJWTAuth(JWTAuth):
    
    #  def __init__(self, expected_audience=None, type_user=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.expected_audience = expected_audience
    #     self.type_user = type_user

    def authenticate(self, request, token):
        """
        Autentica o usuário usando seu modelo CustomUsers.
        """
        try:
            # valida o token e pega o usuário
            user = super().authenticate(request, token)

            if not user:
                raise HttpError(401, _("Invalid token or user does not exist"))
            # opcional: validar audience dentro do token
            if self.expected_audience:
                if token.payload.get("aud") != self.expected_audience:
                    raise HttpError(403, _("Invalid audience"))

            return user
        except Exception:
            raise HttpError(401, _("Invalid token"))