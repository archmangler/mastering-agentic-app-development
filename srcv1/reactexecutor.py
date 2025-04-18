import inspect
import json
from typing import Tuple

from brain import Brain
from common import Agent, AgentConfig, ReactEnd, ToolChoice
from tools import Tool


class ReActExecutor:

    def __init__(self, config: AgentConfig, agent: Agent) -> None:
        self.config = config
        self.base_agent = agent
        self.request = ""
        self.brain = Brain(config)

    @staticmethod
    def __get_tools(agent: Agent) -> list[Tool]:
        tools = [tool for tool in agent.functions if isinstance(tool, Tool)]
        str_tools = [tool.name + " - " + tool.desc for tool in tools]
        return "\n".join(str_tools)

    def __thought(self, current_agent: Agent) -> None:
        tools = self.__get_tools(current_agent)
        prompt = f"""Answer the following request as best you can:  {self.request}.
        First think step by step about what to do.
        Develop and assess your plan.
        Then take the appropriate action.
        Continuously adjust your plan at each step based on the results of your actions, adapting to the new information.
        Your goal is to demonstrate a thorough, adaptive and self reflective problem solving approach, emphasizing dynamic thinking and learning.
        Make sure to use the following tools where appropriate:
        
        {tools}
        
        CONTEXT HISTORY:
        ---
        {self.brain.recall()}
        ---
        """
        response = self.brain.think(prompt=prompt, agent=current_agent)
        print("====================== Begin Thought ==============================")
        print(f"Thought response: {response} \n")
        self.brain.remember("Assistant: " + response)
        print("====================== End Thought ==============================")

    def __action(self, agent: Agent) -> tuple[Agent, bool]:
        tool = self.__choose_action(agent)
        if tool:
            if isinstance(tool.func, Agent):
                agent = tool.func
                print(f"New agent: {agent.name} will now use the tool: {tool.name}")
                return agent, True

            self.__execute_action(tool, agent)
        else:
            print("No tool to execute ...")
            agent = self.base_agent
            return agent, True
        return agent, False

    def __observation(self, current_agent: Agent) -> ReactEnd:
        prompt = f"""Is the context information enough to finally answer to this request: {self.request}?

        Assign a confidence score between 0.0 and 1.0 to guide your approach:

        - 0.8+: Continue with the current approach
        - 0.5-0.7: Consider minor adjustments to the approach
        - Below 0.5: Seriously consider backtracking ans trying a different approach

        CONTEXT HISTORY:
        ---
        {self.brain.recall()}
        ---
        """
        response: ReactEnd = self.brain.think(
            prompt=prompt, agent=current_agent, output_format=ReactEnd
        )
        self.brain.remember("Assistant: " + response.final_answer)
        self.brain.remember("Assistant: " + response.confidence)
        print("====================== Begin Observation ==============================")
        print(f"Observation: {response.final_answer} \n")
        print(f"Approach Confidence score: {response.confidence} \n")
        self.brain.remember("Assistant: " + response)
        print("====================== End Observation ==============================")
        return response

    def execute(self, query_input: str) -> str:
        print(f"Request: {query_input}")
        self.request = query_input
        total_interactions = 0
        agent = self.base_agent
        while True:
            total_interactions += 1
            if self.config.max_interactions <= total_interactions:
                print("Max interactions reached. Exiting ...")
                return ""
            self.__thought(agent)
            agent, skip = self.__action(agent)
            if skip:
                continue
            observation = self.__observation(agent)
            if observation.stop:
                print("I now know the final answer.")
                print(f"Final Answer: {observation.final_answer}")
                return observation.final_answer

    def __choose_action(self, agent: Agent):
        try:
            # Create ToolChoice instance first
            response = ToolChoice(
                tool_name="People_search",
                reason_of_choice="To search for information about Linus Torvalds",
            )

            # Log the action being taken
            message = f""" Assistant: I will use the tool: {response.tool_name} because {response.reason_of_choice}"""
            print(message)

            # Find matching tool
            matching_tools = [
                tool for tool in agent.functions if tool.name == response.tool_name
            ]
            if matching_tools:
                return matching_tools[0]
            else:
                print(
                    f"Warning: Tool {response.tool_name} not found in available tools"
                )
                return None

        except Exception as e:
            print(f"Error in choose_action: {str(e)}")
            return None

    def __execute_action(self, tool: Tool, agent: Agent) -> None:
        if tool is None:
            return
        print(
            f"\n ================== Executing tool: {tool.name} ================== \n "
        )

        prompt = f"""
        To answer the following request as best you can: {self.request}.
        Determine the inputs to send to the tool: {tool.name}.
        Given that the function signature of the tool function is: {inspect.signature(tool.func)}.

        CONTEXT HISTORY:
        ---
        {self.brain.recall()}
        ---
        """

        parameters = inspect.signature(tool.func).parameters
        response = {}

        if len(parameters) > 0:
            prompt += f"""RESPONSE FORMAT:
            {{
                {
                ', '.join([f'"{param}": <function parameter> ' for param in parameters])
                }
            }}
            """
            response = self.brain.think(prompt=prompt, agent=agent)
            self.brain.remember("Assistant: " + response)
            try:
                response = json.loads(response)
            except Exception as e:
                print(f"Error in parsing response: {e}")
                print(f"Invalid response: {response}")
                self.brain.remember(
                    "Assistant: Error in parsing json response: " + response
                )
                return

        action_result = tool.func(**response)
        print(f"Action result: {action_result}")
        msg = f"Assistant: Tool result: {action_result}"
        print(f"Tool Params: {response}")
        print(msg)
        self.brain.remember(f"Assistant: {msg}")
