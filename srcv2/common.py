from typing import Callable, List, Union

from openai import OpenAI
from pydantic import BaseModel, Field
from utils import function_to_json


class ToolChoice(BaseModel):
    """Data Model for Tool Choice"""

    tool_name: str = Field(default=..., description="The name of the tool to use")
    reason_of_choice: str = Field(
        default=..., description="The reason for choosing this tool"
    )


class ReactEnd(BaseModel):
    """Data Model for the  observation step"""

    stop: bool = Field(
        default=...,
        description="True if the context is enough to answer the question else False",
    )
    final_answer: str = Field(
        default=...,
        description="The final answer if the context is enough to answer the question else the partial answer",
    )
    confidence: float = Field(
        default=..., description="The confidence score of the final answer"
    )


class Tool:
    def __init__(self, name: str, func, desc) -> None:
        self.desc = desc
        self.name = name
        self.func = func


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-3.5-turbo"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent"
    functions: List = []
    parallel_tool_calls: bool = True

    def tools_to_json(self):
        return function_to_json(self.functions)


class AgentConfig:
    def __init__(self):
        self.max_interactions = 5
        self.model = None
        self.token_limit: int = 10000

    def with_model_client(self, model: OpenAI):
        self.model = model
        return self

    def with_token_limit(self, token_limit: int):
        self.token_limit = token_limit
        return self

    def with_max_interactions(self, max_int: int):
        self.max_interactions = max_int
        return self

    def with_instructions(self, instructions: Union[str, Callable[[], str]]):
        self.instructions = instructions
        return self

    client = OpenAI()  # This will use your OPENAI_API_KEY environment variable
