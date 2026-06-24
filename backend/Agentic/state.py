from typing import TypedDict


class AgentState(TypedDict):
    question: str
    category: str
    answer: str