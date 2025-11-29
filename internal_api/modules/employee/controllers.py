from typing import Any, List, Tuple
from ninja import Query
from django.db.models import QuerySet
from internal_api.modules.employee.schemas import EmployeeFilter, EmployeeList, EmployeeOutSchema
from internal_api.modules.employee.services import EmployeeService
from internal_api.modules.core.utils.classes import Controller
from ninja_extra import api_controller, route

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
        response=EmployeeOutSchema
    )
    def get(
        self,
        id: int,
    ) -> Tuple[Any, ...]:
        return self.service.get(id=id)