from typing import Any, Optional
from django.db import models, transaction

class Repository:
    model: models.Model

    # @classmethod
    # def update_paylo

class Service:
    repository: Repository

    @classmethod
    def list(cls,*,filters: Optional[Any] = None) -> models.QuerySet:
        queryset = cls.repository.list()
        if filters:
            queryset =filters.filter(queryset)
        return queryset

class Controller:

    service = Service