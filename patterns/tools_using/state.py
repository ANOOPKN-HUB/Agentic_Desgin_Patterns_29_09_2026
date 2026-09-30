from typing import Literal, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    route: Literal["math", "general"]
    expression: str
    answer: str
    result: str