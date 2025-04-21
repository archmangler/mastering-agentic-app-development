import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from agents import triage_agent
from custom_types import Agent, AgentFunction, TaskResponse
from openai import OpenAI
from runner import AppRunner
from tools import (
    case_resolved,
    escalate_to_human,
    initiate_baggage_search,
    initiate_flight_search,
)
from utils import pretty_print_messages


# Storage for agent interactions
class AgentInteractionStore:
    def __init__(self, storage_path: str = "agent_interactions.json"):
        self.storage_path = storage_path
        self.interactions = []
        self._load_storage()

    def _load_storage(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                self.interactions = json.load(f)

    def _save_storage(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.interactions, f, indent=2)

    def record_interaction(
        self,
        agent_name: str,
        messages: List[Dict[str, Any]],
        evaluation: Dict[str, Any],
    ):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "messages": messages,
            "evaluation": evaluation,
        }
        self.interactions.append(interaction)
        self._save_storage()

    def get_interactions(
        self, agent_name: str = None, start_time: str = None, end_time: str = None
    ) -> List[Dict[str, Any]]:
        filtered = self.interactions
        if agent_name:
            filtered = [i for i in filtered if i["agent"] == agent_name]
        if start_time:
            filtered = [i for i in filtered if i["timestamp"] >= start_time]
        if end_time:
            filtered = [i for i in filtered if i["timestamp"] <= end_time]
        return filtered

    def get_metrics_summary(self, time_period: str = "24h") -> Dict[str, Any]:
        """Generate a summary of metrics for the specified time period."""
        end_time = datetime.now()
        if time_period == "24h":
            start_time = end_time - timedelta(hours=24)
        elif time_period == "7d":
            start_time = end_time - timedelta(days=7)
        elif time_period == "30d":
            start_time = end_time - timedelta(days=30)
        else:
            start_time = end_time - timedelta(hours=24)  # Default to 24h

        interactions = self.get_interactions(
            start_time=start_time.isoformat(), end_time=end_time.isoformat()
        )

        if not interactions:
            return {"error": "No interactions found in the specified period"}

        # Calculate average scores
        total_interactions = len(interactions)
        metrics = {
            "total_interactions": total_interactions,
            "average_accuracy": sum(
                i["evaluation"].get("accuracy", 0) for i in interactions
            )
            / total_interactions,
            "average_tool_usage": sum(
                i["evaluation"].get("tool_usage", 0) for i in interactions
            )
            / total_interactions,
            "average_clarity": sum(
                i["evaluation"].get("clarity", 0) for i in interactions
            )
            / total_interactions,
            "average_resolution": sum(
                i["evaluation"].get("resolution", 0) for i in interactions
            )
            / total_interactions,
            "time_period": time_period,
        }

        return metrics


# Reporting Agent
reporting_agent = Agent(
    name="ReportingAgent",
    model="gpt-3.5-turbo",
    instructions="""
    You are responsible for generating reports about agent performance metrics.
    Analyze the provided metrics and generate a clear, concise report that:
    1. Summarizes the key performance indicators
    2. Highlights areas of strength and improvement
    3. Provides actionable insights
    4. Uses clear, non-technical language
    
    Format your response as a well-structured report with sections for:
    - Overview
    - Performance Metrics
    - Key Findings
    - Recommendations
    """,
    description="Agent responsible for generating performance reports",
    functions=[],
)

# Conversation Flow Agent with evaluation capabilities
conversation_flow_agent = Agent(
    name="ConversationFlowAgent",
    model="gpt-3.5-turbo",
    instructions="""
    You are responsible for determining whether a conversation should continue or end,
    and evaluating the quality of agent responses.
    
    For conversation flow:
    Analyze the conversation history and the user's latest response to determine:
    1. If the user's issue has been resolved
    2. If the user wants to end the conversation
    3. If more assistance is needed
    
    For response evaluation:
    Evaluate each agent's response based on:
    1. Accuracy of information provided
    2. Appropriateness of tools used
    3. Clarity and helpfulness of responses
    4. Resolution of user's issues
    
    Consider:
    - The user's explicit statements about resolution
    - The tone and content of their messages
    - Whether the agent has successfully addressed their concerns
    - Any remaining unresolved issues
    
    Return a JSON object with:
    {
        "flow_decision": "continue" or "end",
        "evaluation": {
            "accuracy": score (1-10),
            "tool_usage": score (1-10),
            "clarity": score (1-10),
            "resolution": score (1-10),
            "feedback": "detailed feedback on the interaction"
        }
    }
    """,
    description="Agent responsible for managing conversation flow and evaluating responses",
    functions=[],
)

# Update the main agent with both tools
main_agent = Agent(
    name="MainAgent",
    model="gpt-3.5-turbo",
    instructions="""
    You are a helpful airline assistant that helps customers with their problems.
    
    Available tools:
    1. initiate_baggage_search: Use this tool when customers report lost baggage
    2. initiate_flight_search: Use this tool when customers have issues with their flights
    3. escalate_to_human: Use this tool when you need to transfer the customer to a human agent
    4. case_resolved: Use this tool when the customer's issue has been resolved
    
    Analyze the customer's query carefully and use the appropriate tool to help them.
    If they mention lost baggage, use the initiate_baggage_search tool.
    If they mention flight issues, use the initiate_flight_search tool.
    If you cannot help them, use the escalate_to_human tool with a reason.
    When the issue is resolved, use the case_resolved tool.
    """,
    description="The main agent for the airline application.",
    functions=[
        escalate_to_human,
        initiate_baggage_search,
        initiate_flight_search,
        case_resolved,
    ],
)

# Context variables
context_variables = {
    "customer_context": """Here is what you know about the customer's details:
    1. CUSTOMER_ID: 1234567890
    2. NAME: John Doe
    3. PHONE: 1234567890
    4. EMAIL: john.doe@example.com
    5. FLIGHT_NUMBER: AA123
    6. DEPARTURE_DATE: 2024-01-01
    7. ARRIVAL_DATE: 2024-01-02
    8. DEPARTURE_TIME: 10:00 AM
    9. ARRIVAL_TIME: 12:00 PM
    10. DEPARTURE_AIRPORT: LAX
    11. ARRIVAL_AIRPORT: SFO
    12. FLIGHT_STATUS: ON_TIME
    13. ACCOUNT_STATUS: ACTIVE
    14. ACCOUNT_CREATION_DATE: 2024-01-01
    15. LAST_LOGIN_DATE: 2024-01-01
    16. LAST_LOGIN_IP: 192.168.1.1
    17. LAST_LOGIN_LOCATION: Los Angeles, CA
    18. LAST_LOGIN_DEVICE: MacBook Pro
    19. LAST_LOGIN_BROWSER: Chrome
    20. LAST_LOGIN_USER_AGENT: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
    """
}


def generate_performance_report(runner: AppRunner, metrics: Dict[str, Any]) -> str:
    """Use the reporting agent to generate a performance report."""
    report_messages = [
        {
            "role": "system",
            "content": "Generate a performance report based on the provided metrics.",
        },
        {"role": "user", "content": json.dumps(metrics)},
    ]
    response = runner.run(reporting_agent, report_messages, {})
    return response.messages[-1]["content"]


def evaluate_conversation(runner: AppRunner, messages: list) -> tuple[bool, dict]:
    """Use the conversation flow agent to evaluate the conversation and determine if it should continue."""
    flow_messages = [
        {
            "role": "system",
            "content": "Analyze the conversation and provide evaluation.",
        },
        *messages,
    ]
    response = runner.run(conversation_flow_agent, flow_messages, {})
    try:
        evaluation = json.loads(response.messages[-1]["content"])
        return evaluation["flow_decision"] == "continue", evaluation["evaluation"]
    except json.JSONDecodeError:
        # Fallback if the response isn't valid JSON
        return True, {"error": "Invalid evaluation format"}


def main():
    print("Starting the application...")
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    runner = AppRunner(openai)
    interaction_store = AgentInteractionStore()

    messages = []
    agent = main_agent

    print("\nWelcome to the Airline Assistant! How can I help you today?")
    print(
        "You can end the conversation at any time by indicating you're satisfied or want to exit.\n"
    )
    print(
        "To view performance metrics, type 'metrics' followed by the time period (24h, 7d, or 30d).\n"
    )

    while True:
        # Get user input
        query = input("\nYour request: ").strip()
        if not query:
            continue

        # Check for metrics request
        if query.lower().startswith("metrics"):
            time_period = query.split()[-1] if len(query.split()) > 1 else "24h"
            if time_period not in ["24h", "7d", "30d"]:
                print("Invalid time period. Please use 24h, 7d, or 30d.")
                continue

            metrics = interaction_store.get_metrics_summary(time_period)
            if "error" in metrics:
                print(metrics["error"])
                continue

            report = generate_performance_report(runner, metrics)
            print("\nPerformance Report:")
            print(report)
            continue

        # Process the user's request
        messages.append({"role": "user", "content": query})
        response = runner.run(agent, messages, context_variables)
        messages.extend(response.messages)
        agent = response.agent

        # Print the agent's response
        pretty_print_messages(response.messages)

        # Evaluate the conversation and determine if we should continue
        should_continue, evaluation = evaluate_conversation(runner, messages)

        # Record the interaction and its evaluation
        interaction_store.record_interaction(
            agent_name=agent.name,
            messages=messages[-2:],  # Record the last exchange
            evaluation=evaluation,
        )

        if not should_continue:
            print("\nThank you for using our service. We're glad we could help!")
            break

    print("\nApplication finished.")

    # Print summary of recorded interactions
    print("\nInteraction Summary:")
    interactions = interaction_store.get_interactions()
    for interaction in interactions:
        print(f"\nTime: {interaction['timestamp']}")
        print(f"Agent: {interaction['agent']}")
        print("Evaluation:")
        for key, value in interaction["evaluation"].items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
