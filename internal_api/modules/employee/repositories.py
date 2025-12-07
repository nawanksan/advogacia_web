from django.db import models
from typing import Dict
from django.http import Http404
from internal_api.modules.core.utils.classes import Repository
from internal_api.modules.employee.models import Employee, Role
from internal_api.modules.core.utils.remove_excess_spaces import remove_excess_spaces


class EmployeeRepository(Repository):
    """
    Camada responsável pela comunicação com o banco
    """
    model = Employee
    
    @classmethod
    def update_payload(
        cls, *, payload: Dict, **kwargs
    ) -> Dict:
        """
        Método responsável por remover os
        espaços em excesso dos campos de texto.
        """
        updated_payload: Dict = super().update_payload(
            payload=payload
        )
        updated_payload.update({
            'full_name': remove_excess_spaces(
                updated_payload.get('full_name', '')
            ).upper(),
            'email': remove_excess_spaces(
                updated_payload.get('email', '')
            ).lower(),
        })
        return updated_payload
    
    @classmethod
    def post(
        cls, *, payload: Dict, **kwargs
    ) -> models.Model:
        """
        Método responsável por criar um funcionário.
        """
        instance: models.Model = super().post(
            payload=payload
        )

        return instance

    @classmethod
    def put(
        cls,
        *,
        instance: models.Model,
        payload: Dict,
        **kwargs,
    ) -> models.Model:
        """
        Método responsável por atualizar um funcionário.
        """

        if not isinstance(instance, cls.model):
            raise Http404(
                "The instance does not belong to the model."
                f"{cls.model._meta.verbose_name}."
            )

        instance = super().put(
            instance=instance, payload=payload
        )

        return instance
    
class RoleRepository(Repository):
    """
    Responsável por lidar com a persistência e
    interação com a camada de armazenamento de dados,
    com relação aos cargos de funcionários.
    """

    model = Role

    @classmethod
    def update_payload(
        cls, *, payload: Dict, **kwargs
    ) -> Dict:
        """
        Método responsável por remover os
        espaços em excesso dos campos de texto.
        """
        updated_payload: Dict = super().update_payload(
            payload=payload
        )
        if updated_payload.get('description') is not None:
            updated_payload.update({
                'description': remove_excess_spaces(
                    updated_payload.get('description', '')
                ).upper(),
            })
        updated_payload.update({
            'name': remove_excess_spaces(
                updated_payload.get('name', '')
            ).upper(),
        })
        return updated_payload

    @classmethod
    def disable(
        cls, *, instance: models.Model
    ) -> models.Model:
        """
        Desabilita um registro.
        """
        if not isinstance(instance, cls.model):
            raise Http404(
                "The instance does not belong to the model."
                f"{cls.model._meta.verbose_name}."
            )

        instance.is_active = False
        instance.save()
        return instance
