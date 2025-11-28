from typing import Any, Tuple
from ninja import Query
from django.db.models import QuerySet
from ninja_extra import api_controller, route
from internal_api.modules.core.users.schemas import UserFilter, UserstOutSchema


@api_controller(
    'core/',
    tags=['CORE - USERS']
)
class UserController():
    
    # service = UserService
    
    @route.get(
        'users/',
        response={UserstOutSchema},
        # permissions=[
        #     PostRequestsAccess
        # ]
    )
    def list(self, filters: UserFilter = Query(...)) -> QuerySet[Any]:

        return {"message": "ok"}
    

    @route.get(
        'user/{int:id}',
        response={UserstOutSchema}
    )
    def get(self, id: int, ) -> Tuple[Any, ...]:
        return {"message": "ok"}