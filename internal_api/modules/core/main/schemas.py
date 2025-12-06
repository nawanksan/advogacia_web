from ninja import Schema
from operator import attrgetter, itemgetter
from typing import (
    Any,
    Generic,
    List,
    Optional,
    OrderedDict,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from pydantic import BaseModel


class MessageSchema(Schema):
    message: str


T = TypeVar("T")
class PaginatedResponseSchema(
    Schema,
    BaseModel,
    Generic[T],
):
    """
    Schema responsável por armazenar o Schema (modelo Pydantic) de resposta para a paginação.
    """

    count: int
    results: List[T]
    __generic_model__: Any


PaginatedResponseSchema.__doc__ = ""
PaginatedResponseSchema.__generic_model__ = PaginatedResponseSchema
