import re

def remove_excess_spaces(value: str) -> str:
    if not value:
        return value
    
    value = re.sub(r'\s+', ' ', value)
    return value.strip()