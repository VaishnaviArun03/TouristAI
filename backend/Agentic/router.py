def router(state):
    question = state["question"].lower()

    if any(word in question for word in ["restaurant", "food", "eat"]):
        category = "restaurant"

    elif "hotel" in question:
        category = "hotel"

    elif any(word in question for word in ["book", "booking"]):
        category = "booking"

    else:
        category = "nearby"

    return {
        **state,
        "category": category
    }


def route_question(state):
    return state["category"]