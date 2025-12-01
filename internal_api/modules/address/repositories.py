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

    model = Address

