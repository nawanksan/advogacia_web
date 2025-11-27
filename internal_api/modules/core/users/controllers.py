from typing import Any, Tuple
from ninja_extra import api_controller, route, ControllerBase
from internal_api.modules.core.users.schemas import UsersInPostSchema


@api_controller(
    '/core/users',
    tags=['CORE - USERS']
)
class UserController():
    
    # service = UserService
    
    @route.post(
        '/',
        # response={UserstOutSchema},
        # permissions=[
        #     PostRequestsAccess
        # ]
    )
    def post(
        self,
        request,
        payload: UsersInPostSchema,
    ) -> Tuple[Any, ...]:

        return {"message": "ok"}
