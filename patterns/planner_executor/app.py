"""Command-line demonstration of the planner-executor workflow."""

from .graph import build_graph


if __name__ == "__main__":
    result = build_graph().invoke(
        {"question": "Create a practical three-day plan to learn Python basics."}
    )
    print("\nPlan:")
    for index, step in enumerate(result.get("plan", []), start=1):
        print(f"{index}. {step}")
    print("\nFinal response:")
    print(result.get("answer", "No response was produced."))
