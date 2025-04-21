import copy
import json
from collections import defaultdict
from sys import argv

from custom_types import Agent, AgentFunction, TaskResponse
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from result_handler import ToolCallHandler
from utils import debug_print


class AppRunner:
    def __init__(self, client: OpenAI):
        self.client = client
        # self.result_handler = ToolCallHandler()
        self.tool_handler = ToolCallHandler()

    def run(
        self, agent: Agent, messages: list, variables: dict, max_interactions=10
    ) -> TaskResponse:
        """Execute the conversation loop with improved flow control and error handling."""
        debug_print(True, "AppRunner: Starting execution...")
        # Initialize state
        loop_count = 0
        active_agent = agent
        context_variables = copy.deepcopy(variables)
        history = self.__initialize_message_history(agent, messages, variables)
        init_len = len(messages)

        while loop_count < max_interactions:
            debug_print(True, f"Interaction {loop_count + 1}/{max_interactions}")
            print(f"Active agent: {active_agent}")
            llm_params = self.__create_inference_request(
                active_agent, history, context_variables
            )
            response = self.client.chat.completions.create(**llm_params)
            message: ChatCompletionMessage = response.choices[0].message
            history_msg = json.loads(message.model_dump_json())
            history.append(history_msg)
            loop_count += 1
            if not message.tool_calls:
                debug_print(True, "No tool calls found in response")
                break
            debug_print(True, message.tool_calls)

            response = self.tool_handler.handle_tool_calls(
                message.tool_calls,
                active_agent.functions,
                active_agent,
            )
            debug_print(True, f"response from tool handler: {str(response)}")
            history.extend(response.messages)
            if response.agent:
                active_agent = response.agent

        return TaskResponse(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )

    def __create_inference_request(self, agent: Agent, messages: list, variables: dict):
        """Create OpenAI API request parameters with proper message handling."""
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

    def __initialize_message_history(
        self, agent: Agent, initial_messages: list, variables: dict
    ) -> list:
        """Initialize conversation history ensuring proper system message handling."""
        history = copy.deepcopy(initial_messages)
        context_variables = defaultdict(str, variables)
        system_message = {
            "role": "system",
            "content": agent.get_instructions(context_variables),
        }

        # Only add system message if not present
        if not any(msg.get("role") == "system" for msg in history):
            history.insert(0, system_message)

        return history

    def __process_tool_calls(self, tool_calls: list, agent: Agent) -> list:
        """Process tool calls and return structured results."""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            debug_print(True, f"Processing tool call: {tool_name}")

            tool = next((t for t in agent.functions if t.name == tool_name), None)
            if not tool:
                debug_print(True, f"Tool {tool_name} not found")
                continue

            try:
                debug_print(True, f"Executing tool: {tool_name}")
                result = tool.function()

                # Updated response format to match OpenAI's requirements
                tool_response = {
                    "role": "tool",  # Changed from 'function' to 'tool'
                    "name": tool_name,
                    "tool_call_id": tool_call.id,  # Added tool_call_id
                    "content": (
                        str(result)
                        if not isinstance(result, Agent)
                        else "Switching to new agent"
                    ),
                }

                results.append({"response": tool_response, "result": result})
                debug_print(True, f"Tool execution successful: {tool_response}")

            except Exception as e:
                error_msg = f"Error executing {tool_name}: {str(e)}"
                debug_print(True, error_msg)
                results.append(
                    {
                        "response": {
                            "role": "tool",  # Changed from 'function' to 'tool'
                            "name": tool_name,
                            "tool_call_id": tool_call.id,  # Added tool_call_id
                            "content": f"Error: {str(e)}",
                        },
                        "result": None,
                    }
                )

        return results

    def __should_end_conversation(self, message: ChatCompletionMessage) -> bool:
        """Determine if the conversation should end."""
        if not message.tool_calls and message.content and message.content.strip():
            return True
        return False
