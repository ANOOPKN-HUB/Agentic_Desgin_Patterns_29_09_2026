from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()

def reasoning_agent(state: AgentState):
    prompt = f"""
You are the router and math-reasoning agent for a question-answering workflow.

Decide whether the user's question can be answered by evaluating a single
arithmetic expression using numbers, parentheses, +, -, *, /, //, %, or **.

If it is an arithmetic question, return exactly:
MATH: <arithmetic expression>

If it is anything else (definitions, explanations, writing, general knowledge,
or a question that cannot be represented as one arithmetic expression), return
exactly:
GENERAL

Examples:
Question: What is 5 plus 3?
MATH: 5 + 3
Question: What is the square of the average of 10 and 5?
MATH: ((10 + 5) / 2) ** 2
Question: Define AI.
GENERAL

User question: {state['question']}
Decision:
"""
    decision = str(llm.invoke(prompt).content).strip()
    if decision.upper().startswith("MATH:"):
        expression = decision.split(":", maxsplit=1)[1].strip()
        if expression:
            return {"route": "math", "expression": expression}

    # Treat unrecognized model output as a general question instead of trying
    # to evaluate arbitrary text as Python.
    return {"route": "general"}


def math_agent(state: AgentState):
    result = calculator(state["expression"])
    return {"answer": result, "result": result, "route": "math"}


def fallback_agent(state: AgentState):
    prompt = f"""
Answer the user's question clearly and helpfully. This is the general-question
fallback, so do not produce or execute a Python expression. If the question is
ambiguous, briefly state your assumption.

User question: {state['question']}
Answer:
"""
    answer = str(llm.invoke(prompt).content).strip()
    return {"answer": answer, "route": "general"}