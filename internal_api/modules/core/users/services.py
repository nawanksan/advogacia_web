from internal_api.modules.core.utils.classes import Service
from internal_api.modules.core.users.repositories import UserRepository

class UserService(Service):
    
    repository = UserRepository