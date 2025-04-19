from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from common import Agent
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class TaskResponse(BaseModel):
    """
        Encapsulates the possible responses from a task.
    Attributes:
        messages (str): the response message.
        agent (Agent): the agent instance (if applicable).
        context_variables (dict): a dictionary of context variables.
    """

    messages: List = []
    agent: Optional[Agent] = None
    context_variables: Dict = {}


class FuncResult(BaseModel):
    """
    Encapsulates the possible return values for an agent function.

    Attributes:
        value (str): the response message.
        agent (Agent): the agent instance (if applicable).
        context_variables (dict): a dictionary of context variables.
    """

    value: str = ""
    agent: Optional[Agent] = None
    context_variables: dict = {}
