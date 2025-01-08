from functools import wraps
from typing import get_type_hints, Union

def truncate(value, max_items=10):
    """Helper function to truncate long lists or collections."""
    if isinstance(value, (list, tuple, set)):
        value = list(value)  # Convert to list for slicing
        if len(value) > max_items:
            return value[:max_items] + ["..."]  # Truncate and indicate more items
    return value

def check_type(value, expected_type, max_items=10):
    origin = getattr(expected_type, '__origin__', None)
    args = getattr(expected_type, '__args__', None)

    # If it's a Union or Optional (Union[X, None]), handle that first
    if origin is Union:
        for arg in args:
            is_valid, _ = check_type(value, arg, max_items)
            if is_valid:
                return True, None
        return False, f"Expected one of {args}, got {type(value)}"

    # Now handle other generics (List, Dict, etc.)
    if origin:
        if not isinstance(value, origin):
            return False, f"Expected {origin}, got {type(value)}"

        if args:
            if origin in (list, tuple, set):
                for index, item in enumerate(value):
                    is_valid, error = check_type(item, args[0], max_items)
                    if not is_valid:
                        truncated_value = truncate(value, max_items)
                        return False, f"Item at index {index} in {truncated_value} {error}"
                return True, None
            if origin == dict:
                key_type, value_type = args
                for key, val in value.items():
                    is_valid, error = check_type(key, key_type, max_items)
                    if not is_valid:
                        return False, f"Key '{key}' {error}"
                    is_valid, error = check_type(val, value_type, max_items)
                    if not is_valid:
                        return False, f"Value '{val}' for key '{key}' {error}"
                return True, None
        return True, None

    # Fallback if it's not a generic (e.g. just int, str, etc.)
    if not isinstance(value, expected_type):
        return False, f"Expected {expected_type}, got {type(value)}"
    return True, None

def typecheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        for name, value in zip(arg_names, args):
            if name in hints:
                is_valid, error = check_type(value, hints[name])
                if not is_valid:
                    raise TypeError(f"Argument '{name}' failed type check: {error}")

        for name, value in kwargs.items():
            if name in hints:
                is_valid, error = check_type(value, hints[name])
                if not is_valid:
                    raise TypeError(f"Argument '{name}' failed type check: {error}")

        result = func(*args, **kwargs)

        if 'return' in hints:
            is_valid, error = check_type(result, hints['return'])
            if not is_valid:
                raise TypeError(f"Return value failed type check: {error}")

        return result
    return wrapper
