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
        return ReactEnd(
            stop=True, final_answer="This is the final answer", confidence=0.5
        )

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
        # TODO: implement the logic to choose the action
        response: ToolChoice = ToolChoice(
            tool_name="People_search",
            reason_of_choice="reason_of_choice",
        )
        tool = [tool for tool in agent.functions if tool.name == response.tool_name]
        return tool[0] if tool else None

    def __execute_action(self, tool: Tool, agent: Agent) -> None:
        if tool is None:
            return
        parameters = inspect.signature(tool.func).parameters

        # TODO: Ask ChatGPT to get the parameters values
        response = f"""
        {{
        { ', '.join([f'"{param}": <function parameter value>' for param in parameters]) }
        }}
        """

        try:
            resp = json.loads(response)
        except json.JSONDecodeError:
            print("Error in setting the parameters from ChatGPT")
            print(f"Invalid response: {response}")
            return
        action_reult = tool.func(**resp)
        print(f"Action result: {action_reult}")
