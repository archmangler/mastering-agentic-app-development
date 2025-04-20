# Note: This file is not used in the current implementation
from .utils import debug_print


class ToolCallHandler:

    @staticmethod
    def __handle_function_result(result) -> FuncResult:
        if isinstance(result, FuncResult):
            return result

        if isinstance(result, Agent):
            agent: Agent = result
            return FuncResult(
                value=json.dumps({"assistant": agent.name}),
                agent=agent,
            )

        try:
            return FuncResult(value=str(result))
        except Exception as e:
            error_message = f"Error converting result to FuncResult: {result}"
            debug_print(True, error_message)
            raise TypeError(error_message)

    def handle_tool_calls(
        self,
        tool_calls: ChatCompletionMessageToolCall,
        functions: List[AgentFunction],
        active_agent: Agent,
    ) -> TaskResponse:
        functions_map = {f.__name__: f for f in functions}
        partial_response = TaskResponse(messages=[], agent=None, context_variables={})
        for tool_call in tool_calls:
            self.__handle_call(tool_call, functions_map, partial_response)
        return partial_response

    def __handle_call(
        self,
        tool_call: ChatCompletionMessageToolCall,
        functions_map: dict,
        partial_response: TaskResponse,
    ):
        name = tool_call.function.name
        if name not in function.map:
            debug_print(True, f"Tool {name} not found")
            partial_response.messages.append(
                {
                    "role": "tool",
                    "content": f"Error: tool {name} not found",
                    "tool_name": name,
                    "tool_call_id": tool_call.id,
                }
            )
            return
        raw_result = self.__execute_tool(function_map, name, tool_call)
        result = self.__handle_function_result(raw_result)
        partial_response.messages.append(
            {
                "role": "tool",
                "content": result.value,
                "tool_name": name,
                "tool_call_id": tool_call.id,
            }
        )
        if result.agent:
            partial_response.agent = result.agent

    @staticmethod
    def __execute_tool(function_map, name, tool_call: ChatCompletionMessageToolCall):
        args = json.loads(tool_call.function.parameters)
        debug_print(True, f"Executing tool {name} with args {args}")
        return function_map[name](**args)
