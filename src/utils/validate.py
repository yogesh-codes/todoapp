def isPositiveInt(value):
    if not isinstance(value, int):
        raise ValueError(f"unit value Input must be an integer.")
    if value < 0:
        raise ValueError("units value Input cannot be negative.")
    return value
    