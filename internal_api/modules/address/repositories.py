from typing import Dict

from django.db import models
from django.http import Http404

from core.utils.classes import Repository
from .models import Address,Neighbordhood, City, FederativeUnit ,AbstractBaseModel


class FederativeUnitRepository(Repository):

    model = FederativeUnit


class CityRepository(Repository):

    model = City


class NeighborhoodRepository(Repository):

    model = Neighbordhood


class AddressRepository(Repository):
    """
    Responsável por lidar com a persistência e interação
    com a camada de armazenamento de dados, relacionados
    ao submódulo de endereço.
    """

    model = Address

