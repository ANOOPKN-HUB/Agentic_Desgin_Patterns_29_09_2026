import re

from config.llm import get_llm
from .state import PlannerExecutorState


llm = get_llm()
MAX_PLAN_STEPS = 8


def _parse_plan(content: str) -> list[str]:
    steps = []
    for line in content.splitlines():
        step = re.sub(r"^\s*(?:(?:step\s*)?\d+[.) :\-]+|[-*]\s*)", "", line, flags=re.IGNORECASE).strip()
        if step:
            steps.append(step)
    if not steps and content.strip():
        steps = [content.strip()]
    return steps[:MAX_PLAN_STEPS]


def planner_agent(state: PlannerExecutorState) -> dict:
    response = llm.invoke(
        """You are a careful planning agent. Break the user's request into a concise,
ordered plan of 2 to 6 actionable steps. Return only the numbered steps, one per
line. Do not answer the request yet.

User request:
""" + state["question"]
    )
    plan = _parse_plan(str(response.content))
    if not plan:
        raise ValueError("The planner did not produce any actionable steps.")
    return {"plan": plan, "execution_results": []}


def executor_agent(state: PlannerExecutorState) -> dict:
    execution_results = []
    plan_text = "\n".join(f"{index}. {step}" for index, step in enumerate(state["plan"], 1))

    for index, step in enumerate(state["plan"], 1):
        previous_steps = "\n".join(
            f"Step {result['step_number']}: {result['step']}\nResult: {result['result']}"
            for result in execution_results
        ) or "No steps completed yet."
        response = llm.invoke(
            f"""You are an executor working through a plan. Complete only the current
step. Use the request and earlier step results as context. Be concrete and concise.

Original request: {state['question']}
Full plan:
{plan_text}

Current step {index}: {step}
Earlier execution results:
{previous_steps}

Result for current step:
"""
        )
        execution_results.append(
            {
                "step_number": str(index),
                "step": step,
                "result": str(response.content).strip(),
            }
        )

    return {"execution_results": execution_results}


def response_agent(state: PlannerExecutorState) -> dict:
    work = "\n\n".join(
        f"Step {item['step_number']}: {item['step']}\nExecution result: {item['result']}"
        for item in state["execution_results"]
    )
    response = llm.invoke(
        f"""Answer the user's original request using the completed plan and execution
results below. Synthesize the useful findings into a clear final response. Do not
repeat the plan mechanically.

User request: {state['question']}

Completed work:
{work}

Final response:
"""
    )
    return {"answer": str(response.content).strip()}