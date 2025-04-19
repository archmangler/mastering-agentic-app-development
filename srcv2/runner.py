import copy
import json
from collections import defaultdict
from sys import argv

from common import Agent
from custom_types import AgentFunction, TaskResponse
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from utils import debug_print


class AppRunner:
    def __init__(self, client: OpenAI):
        self.client = client

    def run(
        self, agent: Agent, messages: list, variables: dict, max_interactions=10
    ) -> TaskResponse:
        debug_print(True, "AppRunner: Starting execution...")
        loop_count = 0
        active_agent = agent
        context_variables = copy.deepcopy(variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        while loop_count < max_interactions:
            debug_print(True, f"Interaction {loop_count + 1}/{max_interactions}")
            llm_params = self.__create_inference_request(
                agent, messages, context_variables
            )
            debug_print(True, "Sending request to OpenAI...")
            response = self.client.chat.completions.create(**llm_params)
            debug_print(True, "Received response from OpenAI")
            message = response.choices[0].message
            debug_print(True, "Response from OpenAI:", str(response))
            message.sender = active_agent.name
            history_msg = json.loads(message.model_dump_json())
            history.append(history_msg)

            loop_count += 1
            if not message.tool_calls:
                debug_print(True, "No tool calls found in response, breaking ...")
                break
            debug_print(True, message.tool_calls)
            break
        debug_print(True, "AppRunner: Execution completed")
        return TaskResponse(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )

    def __create_inference_request(self, agent: Agent, messages: list, variables: dict):
        context_variables = defaultdict(str, variables)
        instructions = agent.get_instructions(context_variables)
        messages = [{"role": "system", "content": instructions}] + messages
        tools = agent.tools_to_json()

        debug_print(True, "Creating inference request with messages:", str(messages))
        debug_print(True, "Tools available:", str(tools))

        params = {
            "model": agent.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": agent.tool_choice,
        }

        if tools:
            params["parallel_tool_calls"] = agent.parallel_tool_calls

        return params
