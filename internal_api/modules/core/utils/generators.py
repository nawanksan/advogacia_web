import secrets
import string

def generate_user_password(length: int = 12) -> str:
    """
    Gera uma senha aleatória segura.
    length: tamanho da senha (padrão: 12)
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))