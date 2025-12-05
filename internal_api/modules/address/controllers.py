from ninja_extra import api_controller, route
from typing import Any, List, Tuple
from django.db.models import QuerySet
from ninja import Query


from internal_api.modules.address.schemas import AddressFilter, AddressInPost, AddressInPut, AddressList, AddressOut, CityFilter, CityInPost, CityInPut, CityList, CityOut, CountryFilter, CountryInPost, CountryInPut, CountryList, CountryOut, FederativeUnitInPost, FederativeUnitInPut, FederativeUnitList, FederativeUnitOut, NeighborhoodFilter, NeighborhoodInPost, NeighborhoodInPut, NeighborhoodList, NeighborhoodOut
from internal_api.modules.address.services import AddressService, CityService, CountryServices, FederativeUnitService, NeighborhoodService
from internal_api.modules.core.main.schemas import MessageSchema, PaginatedResponseSchema
from internal_api.modules.core.utils.classes import Controller
from internal_api.modules.core.utils.constants import ERROR_STATUSES, SUCCESS_STATUSES


@api_controller(
    'core/addresses/',
    tags=['ADDRESS - ADDRESS'],

)
class CountryController(Controller):
    """
    Responsável por controlar as requisições relacionadas ao submódulo de país,
    a qual as recebe e coordena as ações necessárias.
    """

    service: CountryServices

    @route.get(
        'country/',
        response=PaginatedResponseSchema[CountryList],
        # permissions=[
        #     GetAddressesAccess
        #     | PostClientsAccess
        #     | PutClientsAccess
        #     | PostGroupCompaniesAccess
        #     | PutGroupCompaniesAccess
        #     | PostUrbanCleaningRouteAccess
        #     | PutUrbanCleaningRouteAccess
        #     | PostEmployeesAccess
        #     | PutEmployeesAccess,
        # ],
    )
    # @paginate(CustomPagination)
    # @ordering(
    #     Ordering,
    #     ordering_fields=[
    #         'id',
    #         'name',
    #         'abbreviation',
    #     ],
    # )
    def list(
        self,
        filters: CountryFilter = Query(...),
    ) -> QuerySet[Any]:
        """
        Rota responsável por fazer a listagem de países.
        ----------------------------------------------

            **Campos de ordenação:**

                - id

                - name

                - abbreviation

                Para ordenar por um campo específico de forma crescente,
                basta passar o nome do campo como parâmetro na requisição.

                *Exemplo: .../country/?ordering=id*

                Para ordenação decrescente, basta passar o nome do campo com o prefixo "-" (hífen).

                *Exemplo: .../country/?ordering=-id*
        """  # noqa: E501
        return self.service.list(filters=filters)

    @route.get(
        'country/{int:id}',
        response={
            SUCCESS_STATUSES: CountryOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[
        #     GetAddressesAccess,
        # ],
    )
    def get(
        self,
        id: int,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por detalhar um país.
        --------------------------------------
        """
        return self.service.get(id=id)

    @route.post(
        'country/',
        response={
            SUCCESS_STATUSES: CountryOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[PostAddressesAccess],
    )
    def post(self, request, payload: CountryInPost) -> Tuple[Any, ...]:
        """
        Rota responsável por criar um país.
        -----------------------------------
        -  abbreviation: A sigla permite apenas 3 letras;
        """
        return self.service.post(
            payload=payload.dict(),
            last_user_id=request.user.id,
        )

    @route.put(
        'country/{int:id}',
        response={
            SUCCESS_STATUSES: CountryOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[PutAddressesAccess],
    )
    def put(
        self,
        request,
        id: int,
        payload: CountryInPut,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por atualizar um país.
        --------------------------------------
        -  abbreviation: A sigla permite apenas 3 letras;
        """
        return self.service.put(
            id=id,
            payload=payload.dict(),
            last_user_id=request.user.id,
        )

    @route.patch(
        'country/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: CountryOut,
            ERROR_STATUSES: MessageSchema,
        },
        # permissions=[DisabledAddressesAccess],
    )
    def disable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        """
        Rota responsável por desabilitar um país.
        -----------------------------------------
        """
        return self.service.disable(
            id=id,
            last_user_id=request.user.id,
        )


@api_controller(
    'address/federative-Unit',
    tags=['ADDRESS - ADDRESS']
)
class FederativeUnitController(Controller):
    
    service = FederativeUnitService
    
    @route.get(
        '/',
        response=List[FederativeUnitList]
    )
    def list(self, filters: CityFilter = Query(...)) -> QuerySet[Any]:
    
        return self.service.list(filters=filters).distinct()
    
    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: FederativeUnitOut,
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
            SUCCESS_STATUSES: FederativeUnitOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def post(
        self,
        request,
        payload: FederativeUnitInPost
    ) -> Tuple[Any, ...]:
        
        return self.service.post(
            payload=payload.dict()
        )
        
    @route.put(
        '/',
        response={
            SUCCESS_STATUSES: FederativeUnitOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def put(
        self,
        request,
        id: int,
        payload: FederativeUnitInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict()
        )
        
    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: FederativeUnitOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def desable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id
        )


@api_controller(
    'address/city',
    tags=['ADDRESS - ADDRESS']
)
class CityController(Controller):
    
    service = CityService
    
    @route.get(
        '/',
        response=List[CityList]
    )
    def list(self, filters: CityFilter = Query(...)) -> QuerySet[Any]:
    
        return self.service.list(filters=filters).distinct()
    
    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: CityOut,
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
            SUCCESS_STATUSES: CityOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def post(
        self,
        request,
        payload: CityInPost
    ) -> Tuple[Any, ...]:
        
        return self.service.post(
            payload=payload.dict()
        )
        
    @route.put(
        '/',
        response={
            SUCCESS_STATUSES: CityOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def put(
        self,
        request,
        id: int,
        payload: CityInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict()
        )
        
    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: CityOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def desable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id
        )

@api_controller(
    'address/neighborhood',
    tags=['ADDRESS - ADDRESS']
)
class NeighborhoodController(Controller):
    
    service = NeighborhoodService
    
    @route.get(
        '/',
        response=List[NeighborhoodList]
    )
    def list(self, filters: NeighborhoodFilter = Query(...)) -> QuerySet[Any]:
    
        return self.service.list(filters=filters).distinct()
    
    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: NeighborhoodOut,
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
            SUCCESS_STATUSES: NeighborhoodOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def post(
        self,
        request,
        payload: NeighborhoodInPost
    ) -> Tuple[Any, ...]:
        
        return self.service.post(
            payload=payload.dict()
        )
        
    @route.put(
        '/',
        response={
            SUCCESS_STATUSES: NeighborhoodOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def put(
        self,
        request,
        id: int,
        payload: NeighborhoodInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict()
        )
        
    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: NeighborhoodOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def desable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id
        )

@api_controller(
    'address/',
    tags=['ADDRESS - ADDRESS']
)
class AddressController(Controller):
    
    service = AddressService
    
    @route.get(
        '/',
        response=List[AddressList]
    )
    def list(self, filters: AddressFilter = Query(...)) -> QuerySet[Any]:
    
        return self.service.list(filters=filters).distinct()
    
    @route.get(
        '/{int:id}',
        response={
            SUCCESS_STATUSES: AddressOut,
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
            SUCCESS_STATUSES: AddressOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def post(
        self,
        request,
        payload: AddressInPost
    ) -> Tuple[Any, ...]:
        
        return self.service.post(
            payload=payload.dict()
        )
        
    @route.put(
        '/',
        response={
            SUCCESS_STATUSES: AddressOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def put(
        self,
        request,
        id: int,
        payload: AddressInPut
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id,
            payload=payload.dict()
        )
        
    @route.patch(
        '/{int:id}/disable/',
        response={
            SUCCESS_STATUSES: AddressOut,
            ERROR_STATUSES: MessageSchema,
        }
    )
    def desable(
        self,
        request,
        id: int,
    ) -> Tuple[Any, ...]:
        
        return self.service.put(
            id=id
        )
