from typing import Any, List, Tuple
from ninja import Query
from django.db.models import QuerySet
from internal_api.modules.employee.schemas import EmployeeFilter, EmployeeInPost, EmployeeInPut, EmployeeList, EmployeeOutSchema, RoleFilter, RoleInPost, RoleInPut, RoleList, RoleOut
from internal_api.modules.employee.services import EmployeeService, RoleService
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
        
@api_controller(
    'employee/role',
    tags=['EMPLOYEE - EMPLOYEE']

)
class RoleController(Controller):
    """
    Responsável por controlar as requisições
    relacionadas aos cargos de funcionários,
    a qual as recebe e coordena as ações necessárias.
    """

    service = RoleService

    @route.get(
        '/',
        response=List[RoleList],
        # permissions=[
        #     GetRolesAccess
        #     | PostEmployeesAccess
        #     | PutEmployeesAccess
        #     | GetRolesPermissionsAccess
        #     | PostRolesPermissionsAccess
        #     | PutRolesPermissionsAccess,
        # ],
    )
    # @paginate(CustomPagination)
    # @ordering(
    #     Ordering,
    #     ordering_fields=[
    #         'id',
    #         'name',
    #         'description',
    #     ],
    # )
    def list(self, filters: RoleFilter = Query(...)) -> QuerySet[Any]:
        """
        Rota responsável por fazer a listagem de cargos de funcionários.
        ---------------------------------------------------------------

        **Campos de ordenação:**

        - id
        - name
        - description

        Para ordenar por um campo específico de forma crescente,
        basta passar o nome do campo como parâmetro na requisição.

        *Exemplo: .../role/?ordering=id*

        Para ordenação decrescente, basta
        passar o nome do campo com o prefixo "-" (hífen).

        *Exemplo: .../role/?ordering=-id*
        """
        return self.service.list(filters=filters)

    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: RoleOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[
        #     GetRolesAccess
        #     | GetRolesPermissionsAccess
        #     | PutRolesPermissionsAccess,
        # ],
    )
    def get(
        self,
        id: int,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por buscar um cargo de funcionário.
        ----------------------------------------------------
        """
        return self.service.get(id=id)

    @route.post(
        '/',
        response={
            SUCCESS_STATUSES: RoleOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[PostRolesAccess],
    )
    def post(self, request, payload: RoleInPost) -> Tuple[Any, ...]:
        """
        Rota responsável por criar um cargo de funcionário.
        ---------------------------------------------------
        """
        return self.service.post(
            payload=payload.dict(),
            # last_user_id=request.user.id,
        )

    @route.put(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: RoleOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[PutRolesAccess],
    )
    def put(
        self,
        request,
        id: int,
        payload: RoleInPut,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por atualizar um cargo de funcionário.
        -------------------------------------------------------
        """
        return self.service.put(
            id=id,
            payload=payload.dict(),
            # last_user_id=request.user.id,
        )

    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: RoleOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[DisableRolesAccess],
    )
    def disable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por inativar um cargo de funcionário.
        -------------------------------------------------------
        """
        return self.service.disable(
            id=id,
            # last_user_id=request.user.id,
        )
