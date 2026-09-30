from typing import TypedDict


class PlannerExecutorState(TypedDict, total=False):
    question: str
    plan: list[str]
    execution_results: list[dict[str, str]]
    answer: str