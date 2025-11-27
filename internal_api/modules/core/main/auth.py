from ninja_extra import api_controller
from ninja_jwt.authentication import JWTAuth
from django.utils.translation import gettext_lazy as _
from ninja.errors import HttpError
# from ninja_jwt.controller import NinjaJWTDefaultController

class  JWTAuth(JWTAuth):

    def authenticate(self, request, token):
        """
        Aqui você autentica usando sua tabela User.
        """
        validated_token =  self.get_validated_token(token)
        user = super().authenticate(request, token)
        if not validated_token:
            raise HttpError(401, _('Invalid token'))
        return user