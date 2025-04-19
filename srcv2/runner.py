import copy
from sys import argv
from common import Agent
from custom_types import AgentFunction, TaskResponse
from openai import OpenAI
from utils import debug_print

class AppRunner:
    def __init__(self, client: OpenAI):
        self.client = client

    def run(
        self, query: str, agent: Agent, variables: dict, messages: list
    ) -> TaskResponse:
        loop_count = 0
        
        active_agent = agent
        context_variables = copy.deepcopy(variables)
        history = copy.deepcopy(messages)
        init_len = len(messages)

        while loop_count < max_interactions:
            llm_params = self.__create_inference_request(agent, messages, variables)
            loop_count += 1
            response = self.client.chat.completions.create(**llm_params)
            debug_print(True, "Response from OpenAI:", str(response))
            messages.extend(response.messages)
            agent = response.agent
            return TaskResponse()

    def __create_inference_request(self, agent: Agent, messages: dict[], variables: dict[]):
        context_variables = defaultdict(str, variables)
        instructions = agent.get_instructions(context_variables)
        messages = [{"role": "system", "content": instructions}] + messages
        tools = agent.tools_in_json()

        debug_print(debug=True, argv=f"Getting chat completion for ...:{str(messages)}")

        params = {
            "model": agent.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": agent.tool_choice
            }    
        
        if tools:
            params["parallel_tool_calls"] = agent.parallel_tool_calls

        return params
