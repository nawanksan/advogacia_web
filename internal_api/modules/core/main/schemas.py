from ninja import Field, Schema
from django.db.models import QuerySet
from operator import attrgetter, itemgetter
from ninja.pagination import PaginationBase
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
from ninja.types import DictStrAny
from django.http import HttpRequest
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

class CustomPagination(PaginationBase):
    """
    Responsável para definição do Schema (modelo Pydantic) de paginação customizado.
    Page size se não for informado, retorna todos os registros. Caso page_size seja informado
    for menor que 1 vai retornar todos os registros. Caso contrário, vai retornar a quantidade
    de registros informada em page_size.
    """

    class Input(Schema):  # pylint: disable=missing-class-docstring
        page: int = Field(1, ge=1, description="Número da página")
        page_size: int = Field(
            100, description="Quantidade de registros por página"
        )

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        request: Optional[HttpRequest] = None,
        **params: DictStrAny,
    ) -> Any:
        assert request, "request is required!"

        offset = None
        results = None

        if pagination.page_size is not None and pagination.page_size > 0:
            offset = (pagination.page - 1) * pagination.page_size

        if offset is not None:
            results = list(
                queryset[offset : offset + pagination.page_size]  # noqa: E203
            )  # noqa: E203
        else:
            results = list(queryset)

        return OrderedDict(
            [
                ("count", queryset.count()),
                ("results", results),
            ]
        )

    @classmethod
    def get_response_schema(
        cls,
        response_schema: Union[Type[Schema], Type[Any]],
    ) -> Any:
        """
        Método responsável por retornar o Schema (modelo Pydantic) de resposta para a paginação.
        """
        return PaginatedResponseSchema[response_schema]