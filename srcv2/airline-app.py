import os

from common import Agent
from custom_types import AgentFunction, TaskResponse
from openai import OpenAI
from runner import AppRunner


def transfer_to_lost_baggage():
    print("Executing lost baggage transfer...")  # Debug print
    return "I will transfer you to the lost baggage department."


def transfer_to_cancelled_flights():
    print("Executing cancelled flights transfer...")  # Debug print
    return "I will transfer you to the cancelled flights department."


# Define the tools with proper structure
lost_baggage_tool = AgentFunction(
    name="transfer_to_lost_baggage",
    description="Transfer the customer to the lost baggage department when they report lost baggage",
    function=transfer_to_lost_baggage,
)

cancelled_flights_tool = AgentFunction(
    name="transfer_to_cancelled_flights",
    description="Transfer the customer to the cancelled flights department when they have issues with cancelled flights",
    function=transfer_to_cancelled_flights,
)

# Update the main agent with both tools
main_agent = Agent(
    name="MainAgent",
    model="gpt-3.5-turbo",  # Specify the model explicitly
    instructions="""
    You are a helpful airline assistant that helps customers with their problems.
    
    Available tools:
    1. transfer_to_lost_baggage: Use this tool when customers report lost baggage
    2. transfer_to_cancelled_flights: Use this tool when customers have issues with cancelled flights
    
    Analyze the customer's query carefully and use the appropriate tool to help them.
    If they mention lost baggage, use the transfer_to_lost_baggage tool.
    If they mention cancelled flights, use the transfer_to_cancelled_flights tool.
    """,
    description="The main agent for the airline application.",
    functions=[lost_baggage_tool, cancelled_flights_tool],  # Add both tools here
)

# Context variables
context_variables = {
    "user_name": "John Doe",
    "flight_number": "AA123",
}


def main():
    print("Starting the application...")
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    runner = AppRunner(openai)

    messages = []
    while True:
        query = "I lost my baggage, what should I do?"
        print(f"\nUser query: {query}")
        messages.append({"role": "user", "content": query})

        print("Sending request to assistant...")
        response = runner.run(
            agent=main_agent, messages=messages, variables=context_variables
        )

        if response.messages:
            print("\nAssistant response:")
            for msg in response.messages:
                print(f"{msg.get('role', 'assistant')}: {msg.get('content', '')}")
                if "function_call" in msg:
                    print(f"Function called: {msg['function_call']}")

        messages.extend(response.messages)
        break

    print("\nApplication finished.")


if __name__ == "__main__":
    main()
