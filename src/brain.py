from typing import Optional, Type

from pydantic import BaseModel

from common import Agent, AgentConfig


class Brain:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.messages = []

    def remember(self, message: str):
        self.messages.append(message)

    def recall(self) -> str:
        return "\n".join(self.messages)

    def think(
        self, prompt: str, agent: Agent, output_format: Optional[Type[BaseModel]] = None
    ) -> str:
        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": prompt},
        ]
        openai_params = {
            "model": agent.model,
            "temperature": 0.1,
            "max_tokens": self.config.token_limit,
            "messages": messages,
        }
        if output_format:
            openai_params["response_format"] = output_format
            completion = self.config.model.chat.completions.parse(**openai_params)
            return completion.choices[0].message.parsed

        completion = self.config.model.chat.completions.create(**openai_params)
        return completion.choices[0].message.content
