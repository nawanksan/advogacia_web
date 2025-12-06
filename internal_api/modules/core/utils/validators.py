import re


def validate_email(email: str) -> bool:
    """
    Valida emails. Retorna True ou False.
    """

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False


def validate_username(username: str) -> bool:
    """
    Valida nomes de usuário permitindo apenas letras minúsculas sem
    espaços e min_length=5, max_length=60.
    """

    if not (len(username) >= 5 and len(username) <= 60):
        return False
    pattern = r'^[a-z]+$'
    if re.match(pattern, username):
        return True
    else:
        return False


def validate_password(password: str) -> bool:
    """
    Valida senhas com mais de 8 caracteres que contêm letras, números e
    caractere especial.
    """

    # Checks that the password is at least 8 characters long
    if len(password) < 8:
        return False

    # Checks that the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Checks that the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Checks that the password contains at least one number
    if not re.search(r'\d', password):
        return False

    # Checks if the password contains at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    # If password passes all criteria, return True
    return True
