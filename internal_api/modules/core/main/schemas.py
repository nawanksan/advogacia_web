from ninja import Field, Schema
from django.db.models import QuerySet
from operator import attrgetter, itemgetter
from ninja_extra.pagination import PaginationBase
from django.core.paginator import Paginator
from ninja.pagination import PageNumberPagination

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

class CustomPagination(PaginationBase):
    page_size = 10
    page_size_query_param = "per_page"
    max_page_size = 100

    def get_page_size(self, request):
        try:
            return int(request.GET.get(self.page_size_query_param, self.page_size))
        except:
            return self.page_size

    # PARA NINJA-EXTRA → assinatura obrigatória
    def paginate_queryset(self, queryset, request, **params):
        page_size = self.get_page_size(request)
        paginator = Paginator(queryset, page_size)

        page_number = request.GET.get("page", 1)
        page = paginator.get_page(page_number)

        return page.object_list, paginator, page

    def get_paginated_response(self, data, paginator, page, **params):
        return {
            "count": paginator.count,
            "results": data,
        }

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