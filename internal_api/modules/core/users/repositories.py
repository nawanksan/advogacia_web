from internal_api.modules.core.utils.classes import Repository
from .models import CustomUsers as User

class UserRepository(Repository):
    
    model = User