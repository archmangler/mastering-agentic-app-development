import inspect
import json
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


def pretty_print_messages(messages):
    """Pretty print the messages in a readable format."""
    for message in messages:
        print(f"\n{message['role'].upper()}:")
        if message.get("content"):
            print(message["content"])
        if message.get("tool_calls"):
            for tool_call in message["tool_calls"]:
                print(f"\nTool Call: {tool_call['function']['name']}")
                args = tool_call["function"].get("arguments", "{}")
                try:
                    arg_str = json.dumps(json.loads(args)).replace(":", "=")
                    print(f"Arguments: {arg_str}")
                except json.JSONDecodeError:
                    print(f"Arguments: {args}")
