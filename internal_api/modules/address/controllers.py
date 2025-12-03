from ninja_extra import api_controller, route
from typing import Any, List, Tuple
from django.db.models import QuerySet
from ninja import Query


from internal_api.modules.address.schemas import AddressFilter, AddressList
from internal_api.modules.address.services import AddressService
from internal_api.modules.core.utils.classes import Controller

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