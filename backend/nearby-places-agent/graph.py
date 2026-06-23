from typing import TypedDict
from agent import nearby_places_agent
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    question: str
    answer: str


def search_places(state):
    question = state["question"]

    answer = nearby_places_agent(question)

    return {
        "question": question,
        "answer": answer
    }


graph = StateGraph(AgentState)

graph.add_node(
    "search_places",
    search_places
)

graph.set_entry_point("search_places")

graph.add_edge(
    "search_places",
    END
)

app = graph.compile()