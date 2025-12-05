from typing import Any, List, Tuple
from internal_api.modules.core.main.schemas import PaginatedResponseSchema
from internal_api.modules.core.utils.classes import Controller
from ninja import Query
from django.db.models import QuerySet
from ninja_extra import api_controller, route
from internal_api.modules.core.users.schemas import UserFilter, UsersList, UserstOutSchema
from internal_api.modules.core.users.services import UserService


@api_controller(
    'core/',
    tags=['CORE - USERS']
)
class UserController(Controller):
    
    service = UserService
    
    @route.get(
        'users/',
        response=PaginatedResponseSchema[UsersList],
        # permissions=[
        #     PostRequestsAccess
        # ]
    )
    def list(self, filters: UserFilter = Query(...)) -> QuerySet[Any]:

        return self.service.list(
            filters=filters
        )
    

    @route.get(
        'user/{int:id}',
        response=UserstOutSchema
    )
    def get(self, id: int, ) -> Tuple[Any, ...]:
        return self.service.get(id=id)