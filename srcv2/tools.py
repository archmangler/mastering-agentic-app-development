from custom_types import AgentFunction


def _initiate_baggage_search():
    return "Initiating baggage search..."


def _initiate_flight_search():
    return "Initiating flight search..."


def _escalate_to_human(reason=None):
    return (
        f"Escalating to human agent with reason: {reason}"
        if reason
        else "Escalating to human agent"
    )


def _case_resolved():
    return "Case has been resolved"


# Create AgentFunction objects for each tool
initiate_baggage_search = AgentFunction(
    name="initiate_baggage_search",
    description="Initiate a search for lost baggage",
    function=_initiate_baggage_search,
)

initiate_flight_search = AgentFunction(
    name="initiate_flight_search",
    description="Initiate a search for flight information",
    function=_initiate_flight_search,
)

escalate_to_human = AgentFunction(
    name="escalate_to_human",
    description="Escalate the case to a human agent for further assistance",
    function=_escalate_to_human,
    parameters={
        "type": "object",
        "properties": {
            "reason": {
                "type": "string",
                "description": "The reason for escalating to a human agent",
            }
        },
    },
)

case_resolved = AgentFunction(
    name="case_resolved",
    description="Mark the case as resolved",
    function=_case_resolved,
)
