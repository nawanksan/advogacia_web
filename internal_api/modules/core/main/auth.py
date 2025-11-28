from ninja_extra import api_controller
from ninja_jwt.authentication import JWTAuth
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError
# from ninja_jwt.controller import NinjaJWTDefaultController

class  CustomJWTAuth(JWTAuth):

    def authenticate(self, request, token):
        """
        Autentica o usuário usando seu modelo CustomUsers.
        """
        try:
            # valida o token e pega o usuário
            user = super().authenticate(request, token)
            if not user:
                raise HttpError(401, _("Invalid token or user does not exist"))
            return user
        except Exception:
            raise HttpError(401, _("Invalid token"))