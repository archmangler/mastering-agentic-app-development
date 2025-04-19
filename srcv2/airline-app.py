from common import Agent
from custom_types import AgentFunction, TaskResponse
from openai import OpenAI
from tools import calculator_tool, people_search_tool, today_tool

main_agent = Agent(
    name="MainAgent",
    instructions=f"""
    You are a helpful assistant that assists customers with completing a task using multiple tools.
    """,
    description="The main agent for the airline application.",
    functions=[people_search_tool, calculator_tool, today_tool],
)

context_variables = {
    "name": "Linus Torvalds",
    "age": 52,
    "location": "San Francisco",
    "email": "linus@gmail.com",
    "phone": "+1234567890",
    "address": "123 Main St, San Francisco, CA 94101",
    "zip_code": "94101",
    "country": "United States",
}


class AppRunner:
    def __init__(self, client: OpenAI):
        self.client = client

    def run(
        self, query: str, agent: Agent, variables: dict, messages: list
    ) -> TaskResponse:
        return TaskResponse()


if __name__ == "__main__":
    print("Starting the application...")
    runner = AppRunner(client=OpenAI())
    messages = []
    while True:
        # query = input("Enter a query: ")
        query = "test"
        response = runner.run(query, main_agent, context_variables, messages)
        messages.extend(response.messages)
        agent = response.agent
        break

    print("Application finished.")
