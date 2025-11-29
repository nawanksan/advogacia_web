

from internal_api.modules.core.utils.classes import Service
from internal_api.modules.employee.repositories import EmployeeRepository


class EmployeeService(Service):
    """
    Camada responsável pelas regras de negócio
    """
    repository = EmployeeRepository