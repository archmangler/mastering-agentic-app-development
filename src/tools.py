import datetime

from common import Agent, Tool


def perform_calculator(operation: str, a: int, b: int) -> int:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Invalid operation"


def search_wikipedia(search_query: str):
    try:
        page = wikipedia.page(search_query)
        text = page.content
    except Exception as e:
        return (
            "Could not find any infromation on wikipedia for the search query: "
            + search_query
            + ". Please try another search term."
        )
    return text[:300]


def date_of_today():
    return datetime.date.today().strftime("%Y-%m-%d")


calculator_tool = Tool(
    name="Calculator", func=perform_calculator, desc="Use this to perform calculations"
)

people_search_agent = Agent(
    name="People Search Agent",
    instructions="""
    You are a helpful assistant that can search for people information on wikipedia using the person's name.
    """,
    functions=[calculator_tool],
)

people_search_tool = Tool(
    name="People_search",
    func=people_search_agent,
    desc="Use this to search for people information on wikipedia using the person's name",
)

# Export the tools directly - no need for self-import
__all__ = ["calculator_tool", "people_search_tool"]
