import inspect
from datetime import datetime


def debug_print(debug: bool, *args: str):
    if not debug:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))
    print(f"\033[97m[\033[90m{timestamp}\033[97m\033[90m {message}\033[0m")


def function_to_json(func) -> dict:
    """
    Convert a function to a JSON-serializable dictionary that describes the function's signature, including  its name, description
    and parameters.

    Args:
        func (Callable): The function to be converted.

    Returns:
        dict: A JSON-serializable dictionary that describes the function's signature.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        tuple: "array",
        set: "array",
    }
