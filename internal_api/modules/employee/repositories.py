

from internal_api.modules.core.utils.classes import Repository
from internal_api.modules.employee.models import Employee


class EmployeeRepository(Repository):

    models = Employee