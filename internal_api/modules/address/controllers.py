from ninja_extra import api_controller, route
from typing import Any, List, Tuple
from django.db.models import QuerySet
from ninja import Query


from internal_api.modules.address.schemas import AddressFilter, AddressInPost, AddressInPut, AddressList, AddressOut, CityFilter, CityInPost, CityInPut, CityList, CityOut, FederativeUnitInPost, FederativeUnitInPut, FederativeUnitList, FederativeUnitOut, NeighborhoodFilter, NeighborhoodInPost, NeighborhoodInPut, NeighborhoodList, NeighborhoodOut
from internal_api.modules.address.services import AddressService, CityService, FederativeUnitService, NeighborhoodService
from internal_api.modules.core.main.schemas import MessageSchema
from internal_api.modules.core.utils.classes import Controller
from internal_api.modules.core.utils.constants import ERROR_STATUSES, SUCCESS_STATUSES


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
