from langgraph.graph import StateGraph, END

from state import AgentState
from router import router, route_question

from agents.nearby_agent import nearby_agent
from agents.restaurant_agent import restaurant_agent
from agents.hotel_agent import hotel_agent
from agents.booking_agent import booking_agent


def nearby_node(state):
    return {
        **state,
        "answer": nearby_agent(state["question"])
    }


def restaurant_node(state):
    return {
        **state,
        "answer": restaurant_agent(state["question"])
    }


def hotel_node(state):
    return {
        **state,
        "answer": hotel_agent(state["question"])
    }


def booking_node(state):
    return {
        **state,
        "answer": booking_agent(state["question"])
    }


graph = StateGraph(AgentState)

graph.add_node("router", router)
graph.add_node("nearby", nearby_node)
graph.add_node("restaurant", restaurant_node)
graph.add_node("hotel", hotel_node)
graph.add_node("booking", booking_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route_question,
    {
        "nearby": "nearby",
        "restaurant": "restaurant",
        "hotel": "hotel",
        "booking": "booking"
    }
)

graph.add_edge("nearby", END)
graph.add_edge("restaurant", END)
graph.add_edge("hotel", END)
graph.add_edge("booking", END)

app = graph.compile()