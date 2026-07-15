def camel_to_snake(character: str) -> str:
    result = ''
    for i, char in enumerate(character):
        if char.isupper() and i > 0:
            result += '_' + char.lower()
        else:
            result += char.lower()
    return result
