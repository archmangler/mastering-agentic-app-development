def escalate_to_human(reason=None):
    return (
        f"Escalating to human agent with reason: {reason}"
        if reason
        else "Escalating to human agent"
    )


def transfer_to_lost_baggage():
    pass


def transfer_to_cancelled_flights():
    pass


def case_resolved():
    return "Case resolved. No further questions."


def initiate_baggage_search():
    return "Baggage was found in the lost and found section."


def initiate_flight_search():
    pass
