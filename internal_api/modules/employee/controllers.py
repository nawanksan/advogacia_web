from typing import Any, List, Tuple
from ninja import Query
from django.db.models import QuerySet
from internal_api.modules.employee.schemas import EmployeeFilter, EmployeeInPost, EmployeeInPut, EmployeeList, EmployeeOutSchema
from internal_api.modules.employee.services import EmployeeService
from internal_api.modules.core.utils.classes import Controller
from ninja_extra import api_controller, route

from internal_api.modules.core.utils.constants import ERROR_STATUSES, SUCCESS_STATUSES
from internal_api.modules.core.main.schemas import MessageSchema

@api_controller(
    'employee/',
    tags=['EMPLOYEE - EMPLOYEE']
)
class EmployeeController(Controller):

    service = EmployeeService

    @route.get(
        '/',
        response=List[EmployeeList]
    )
    def list(self, filters: EmployeeFilter = Query(...)) -> QuerySet[Any]:

        return self.service.list(filters=filters)
    

    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: EmployeeOutSchema,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def get(
        self,
        id: int,
    ) -> Tuple[Any, ...]:
        return self.service.get(id=id)
    

    @route.post(
        '/',
        response={
            SUCCESS_STATUSES: EmployeeOutSchema,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def post(
        self,
        request,
        payload: EmployeeInPost
    ) -> Tuple[Any, ...]:
        
        return self.service.post(
            payload=payload.dict(),
            request=request,
        )

    @route.put(
        '/',
        response={
            SUCCESS_STATUSES: EmployeeOutSchema,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def put(
        self,
        request,
        id: int,
        payload: EmployeeInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict(),
            request=request,
        )

    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: EmployeeOutSchema,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def desable(
        self,
        request,
        id: int,
        payload: EmployeeInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict(),
            request=request,
        )