from custom_types import Agent, AgentFunction, TaskResponse
from lost_baggage import LOST_BAGGAGE_POLICY, STARTER_PROMPT
from tools import (
    case_resolved,
    escalate_to_human,
    initiate_baggage_search,
    initiate_flight_search,
)
from utils import pretty_print_messages


def transfer_to_lost_baggage():
    print("Executing lost baggage transfer...")  # Debug print
    return lost_baggage_agent


def transfer_to_triage():
    print("Calling transfer to triage agent ...")  # Debug print
    return triage_agent


# Define the tools with proper structure
lost_baggage_agent = Agent(
    name="Lost baggage Agent",
    instructions=STARTER_PROMPT + LOST_BAGGAGE_POLICY,
    functions=[
        initiate_baggage_search,
        escalate_to_human,
        case_resolved,
        transfer_to_triage,
    ],
)


def triage_instructions():
    customer_context = context_variables.get("customer_context", None)
    flight_context = context_variables.get("flight_context", None)
    return f"""You are to triage a customer's request and call a tool to transfer to the right intent.
     Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
      You don't nee to know specifics, just the topic of the request.
       When you need more information to triage the request to an agent, ask a direct question without explaining why you're it.
        Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of the user!
         The customer context is here: {customer_context} and the flight context is here: {flight_context} """


triage_agent = Agent(
    name="Triage Agent",
    instructions="triage_instructions",
    functions=[
        initiate_baggage_search,
        initiate_flight_search,
        escalate_to_human,
        case_resolved,
    ],
)

# Add to existing agents
reporting_agent = Agent(
    name="ReportingAgent",
    model="gpt-3.5-turbo",
    metrics_enabled=True,
    # ... other fields ...
)
