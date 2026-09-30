# Agentic AI Pattern Lab

A small LangGraph application with a Streamlit interface for demonstrating three agentic patterns: tool-using, planner-executor, and supervisor-worker.

## Features

- **Intent routing:** classifies a question as arithmetic or general-purpose.
- **Math tool:** evaluates basic arithmetic without Python `eval`.
- **General fallback:** answers definitions, explanations, and other non-arithmetic questions.
- **Streamlit UI:** chat-style interface with example prompts and an indicator showing which branch answered.
- **CLI runner:** run the workflow directly from the command line.
- **Planner-executor:** creates an ordered plan, executes each step with prior results as context, then synthesizes a final response.
- **Supervisor-worker:** delegates arithmetic requests to a math worker and leave-balance requests to a leave worker.
- **Pattern switcher:** choose a demonstration from the same Streamlit app.

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- Git (if cloning this repository)

## Setup

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, use `source .venv/bin/activate` to activate the environment.

Create a `.env` file in the repository root and add your API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Keep `.env` private; it is excluded from Git. The workflow uses the `gpt-4o-mini` model, configured in `config/llm.py`.

## Run the Streamlit app

From the repository root with the virtual environment activated:

```powershell
streamlit run app.py
```

Open the local URL Streamlit prints in the terminal. Choose **Tool-Using** for arithmetic and general questions, **Planner-Executor** for multi-step requests, or **Supervisor-Worker** for calculations and sample employee leave-balance lookups. The planner mode displays its plan and step results; the supervisor-worker mode shows the selected worker and its result.

## Run from the command line

Run the sample arithmetic workflow from the repository root:

```powershell
python -m patterns.tools_using.run
```

The older singular module path remains supported as an alias:

```powershell
python -m patterns.tool_using.run
```

The CLI example in `patterns/tools_using/run.py` demonstrates arithmetic. Run the planner-executor example with:

```powershell
python -m patterns.planner_executor.app
```

Run the supervisor-worker examples with:

```powershell
python -m patterns.supervisor_worker.run
```

The graphs can also be imported and invoked from your own code. The tool-using and planner-executor graphs take a `question` field; the supervisor-worker graph takes a `query` field.

## Workflow

```text
Tool-Using pattern:
Question → Reasoning/Router
	├─ arithmetic → Math Agent → Safe Calculator → Answer
	└─ other      → General Fallback             → Answer

Planner-Executor pattern:
Question → Planner → Step Executor (with accumulated context) → Final Synthesis

Supervisor-Worker pattern:
Question → Supervisor ── math ──► Math Worker
					└─ leave ─► Leave-Balance Worker
```

The tool-using graph is defined in `patterns/tools_using/`; the planner-executor graph, state, and agents are in `patterns/planner_executor/`; and the supervisor-worker graph is in `patterns/supervisor_worker/`. Root `app.py` presents all three in Streamlit. The planner limits generated plans to eight steps. The leave worker uses sample records initialized in `tools/leaves_db.py`. The calculator accepts numeric constants, parentheses, unary signs, and `+`, `-`, `*`, `/`, `//`, `%`, and `**`; it rejects other Python syntax and limits expression size and exponent magnitude.

## Configuration and troubleshooting

- **Missing API key:** ensure `.env` is in the repository root and contains `OPENAI_API_KEY=...`. Restart Streamlit after changing it.
- **Module not found:** run commands from the repository root and ensure the virtual environment is active.
- **Wrong runner path:** the directory name is `tools_using` (plural); the singular `tool_using` path is provided only as a compatibility alias.
- **Dependency installation interrupted:** retry `python -m pip install -r requirements.txt` after checking your network connection.

## Security note

The calculator parses a restricted arithmetic AST and does not execute arbitrary Python code. The LLM still processes the text you submit, so avoid entering secrets or sensitive personal information.
