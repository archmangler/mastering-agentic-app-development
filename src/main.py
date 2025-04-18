import os

from openai import OpenAI

from common import Agent, AgentConfig
from reactexecutor import ReActExecutor
from tools import calculator_tool, people_search_tool, today_tool

# store this in your bash environment variables
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

main_agent = Agent(
    name="MultiTool Agent",
    instructions="""
    You are a helpful multi-tool assistance that can use different tools to answer questions
    """,
    functions=[calculator_tool, people_search_tool, today_tool],
)

if __name__ == "__main__":
    query = "What is the double of Linux Torvalds' age?"
    agent_config = AgentConfig().with_model_client(openai).with_token_limit(4000)

    executor = ReActExecutor(agent_config, main_agent)
    result = executor.execute(query)
    print("Final result:", result)
