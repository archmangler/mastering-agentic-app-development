from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel, Field


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-3.5-turbo"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent"
    functions: List = []
    parallel_tool_calls: bool = True
    max_interactions: int = 5
    tool_choice: str = None
    metrics_enabled: bool = False
    evaluation_criteria: Dict[str, Any] = {}

    def tools_to_json(self):
        """Convert the agent's functions to OpenAI's function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": f.name if isinstance(f, AgentFunction) else f.__name__,
                    "description": (
                        f.description
                        if isinstance(f, AgentFunction)
                        else f.__doc__ or ""
                    ),
                    "parameters": (
                        f.parameters
                        if isinstance(f, AgentFunction) and f.parameters
                        else {"type": "object", "properties": {}}
                    ),
                },
            }
            for f in self.functions
        ]

    def get_instructions(self, context_variables: dict = {}) -> str:
        if callable(self.instructions):
            return self.instructions(context_variables)
        return self.instructions


class AgentFunction(BaseModel):
    name: str
    description: str
    function: Callable[[], Union[str, Agent, dict]]
    parameters: Optional[Dict] = None


# Rebuild the model to resolve forward references
AgentFunction.model_rebuild()


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
