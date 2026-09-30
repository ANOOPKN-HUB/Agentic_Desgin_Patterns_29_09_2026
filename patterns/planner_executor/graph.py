from langgraph.graph import END, StateGraph

from .nodes import executor_agent, planner_agent, response_agent
from .state import PlannerExecutorState


def build_graph():
    graph = StateGraph(PlannerExecutorState)
    graph.add_node("planner_agent", planner_agent)
    graph.add_node("executor_agent", executor_agent)
    graph.add_node("response_agent", response_agent)

    graph.set_entry_point("planner_agent")
    graph.add_edge("planner_agent", "executor_agent")
    graph.add_edge("executor_agent", "response_agent")
    graph.add_edge("response_agent", END)
    return graph.compile()