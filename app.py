"""Streamlit interface for the agentic design pattern demonstrations."""

import streamlit as st

from patterns.planner_executor.graph import build_graph as build_planner_graph
from patterns.supervisor_worker.graph import build_graph as build_supervisor_worker_graph
from patterns.tools_using.graph import build_graph


st.set_page_config(
    page_title="Agentic AI Pattern Lab",
    page_icon="✳️",
    layout="centered",
)


@st.cache_resource
def get_workflow():
    return build_graph()


@st.cache_resource
def get_planner_workflow():
    return build_planner_graph()


@st.cache_resource
def get_supervisor_worker_workflow():
    return build_supervisor_worker_graph()


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { color-scheme: dark; }
    .stApp {
        background:
          radial-gradient(ellipse at 14% 8%, rgba(20, 184, 166, .12), transparent 34%),
          radial-gradient(ellipse at 88% 20%, rgba(99, 102, 241, .12), transparent 32%),
          #080d17;
        color: #e6edf7;
        font-family: 'Manrope', sans-serif;
    }
    .block-container { max-width: 820px; padding-top: 3.2rem; padding-bottom: 4rem; }
    .eyebrow { color: #5eead4; font: 500 .76rem 'DM Mono', monospace; letter-spacing: .16em; text-transform: uppercase; }
    .hero { font-size: clamp(2.3rem, 6vw, 4.1rem); line-height: 1.06; font-weight: 800; letter-spacing: -.055em; margin: .6rem 0 .7rem; }
    .hero span { background: linear-gradient(100deg, #5eead4, #93c5fd 65%, #c4b5fd); -webkit-background-clip: text; color: transparent; }
    .subhead { color: #9eacc1; font-size: 1.03rem; line-height: 1.7; max-width: 650px; }
    .status-row { display: flex; gap: .55rem; flex-wrap: wrap; margin: 1.4rem 0 2rem; }
    .pill { font: 400 .75rem 'DM Mono', monospace; color: #c4d1e3; border: 1px solid #263347; background: rgba(18, 28, 44, .8); padding: .45rem .72rem; border-radius: 999px; }
    .stTextArea textarea { background: rgba(14, 23, 37, .92); border: 1px solid #29384f; color: #eef5ff; border-radius: 16px; font-size: 1rem; }
    .stTextArea textarea:focus { border-color: #5eead4; box-shadow: 0 0 0 1px #5eead4; }
    div.stButton > button { border: 0; border-radius: 12px; min-height: 3rem; font-weight: 700; color: #07131c; background: linear-gradient(100deg, #5eead4, #93c5fd); transition: transform .15s ease, filter .15s ease; }
    div.stButton > button:hover { filter: brightness(1.08); transform: translateY(-1px); color: #07131c; }
    [data-testid="stChatMessage"] { background: rgba(15, 24, 39, .84); border: 1px solid #25334a; border-radius: 16px; padding: 1rem; }
    .section-label { color: #9eacc1; font: 500 .76rem 'DM Mono', monospace; letter-spacing: .12em; text-transform: uppercase; margin: 1.5rem 0 .7rem; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">LangGraph · agentic pattern lab</div>', unsafe_allow_html=True)
mode = st.radio(
    "Choose a workflow",
    ("Tool-Using", "Planner-Executor", "Supervisor-Worker"),
    horizontal=True,
    label_visibility="collapsed",
    key="workflow_mode",
)

if mode == "Tool-Using":
    history_key = "tool_messages"
    st.markdown('<div class="hero">Ask. <span>Route. Solve.</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subhead">A reasoning agent routes arithmetic to a calculator and sends other questions to a general-purpose fallback.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="status-row"><span class="pill">01 · Reasoning router</span><span class="pill">02 · Calculator tool</span><span class="pill">03 · General fallback</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Try an example"):
        st.markdown("**Math:** What is the square of the average of 10 and 5?")
        st.markdown("**General:** Define artificial intelligence in one sentence.")
    question = st.text_area(
        "Your question",
        placeholder="Ask a math question or anything else…",
        height=112,
        label_visibility="collapsed",
        key="tool_question_input",
    )
    submit = st.button("✦  Ask the assistant", use_container_width=True, type="primary", key="tool_submit")
    if submit:
        if not question.strip():
            st.warning("Enter a question to get started.")
        else:
            with st.spinner("Choosing the right path and preparing an answer…"):
                try:
                    result = get_workflow().invoke({"question": question.strip()})
                    answer = result.get("answer") or result.get("result") or "I couldn't produce an answer. Please try rephrasing."
                    st.session_state.setdefault(history_key, []).append(
                        {"question": question.strip(), "answer": str(answer), "route": result.get("route", "general")}
                    )
                except Exception as error:
                    st.error(f"The assistant could not complete the request. Check OPENAI_API_KEY. Details: {error}")

    if st.session_state.get(history_key):
        st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)
        for message in st.session_state[history_key]:
            with st.chat_message("user"):
                st.markdown(message["question"])
            with st.chat_message("assistant"):
                st.markdown(message["answer"])
                route_label = "Math tool" if message["route"] == "math" else "General fallback"
                st.caption(f"Answered via · {route_label}")
elif mode == "Planner-Executor":
    history_key = "planner_messages"
    st.markdown('<div class="hero">Plan. <span>Execute. Deliver.</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subhead">A planner breaks a request into ordered steps, an executor works through them with accumulated context, and a final agent synthesizes the result.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="status-row"><span class="pill">01 · Planner</span><span class="pill">02 · Step executor</span><span class="pill">03 · Final synthesis</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Try an example"):
        st.markdown("**Research:** Compare solar and wind energy for a small home.")
        st.markdown("**Writing:** Create a 3-day study plan for learning Python basics.")
    question = st.text_area(
        "Your request",
        placeholder="Describe a task that benefits from a few ordered steps…",
        height=112,
        label_visibility="collapsed",
        key="planner_question_input",
    )
    submit = st.button("✦  Plan and execute", use_container_width=True, type="primary", key="planner_submit")
    if submit:
        if not question.strip():
            st.warning("Enter a request to get started.")
        else:
            with st.spinner("Planning the work, executing each step, and preparing a response…"):
                try:
                    result = get_planner_workflow().invoke({"question": question.strip()})
                    st.session_state.setdefault(history_key, []).append(
                        {
                            "question": question.strip(),
                            "answer": result.get("answer", "No final response was produced."),
                            "plan": result.get("plan", []),
                            "execution_results": result.get("execution_results", []),
                        }
                    )
                except Exception as error:
                    st.error(f"The planner workflow could not complete the request. Check OPENAI_API_KEY. Details: {error}")

    if st.session_state.get(history_key):
        st.markdown('<div class="section-label">Execution trace</div>', unsafe_allow_html=True)
        for message in st.session_state[history_key]:
            with st.chat_message("user"):
                st.markdown(message["question"])
            with st.chat_message("assistant"):
                st.markdown(message["answer"])
                with st.expander(f"View plan and execution · {len(message['plan'])} steps"):
                    for step_result in message["execution_results"]:
                        st.markdown(f"**{step_result['step_number']}. {step_result['step']}**")
                        st.write(step_result["result"])
                        if step_result != message["execution_results"][-1]:
                            st.divider()
else:
    history_key = "supervisor_worker_messages"
    st.markdown('<div class="hero">Delegate. <span>Specialize. Resolve.</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subhead">A supervisor classifies each request and delegates it to a math specialist or a leave-balance specialist.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="status-row"><span class="pill">01 · Supervisor</span><span class="pill">02 · Math worker</span><span class="pill">03 · Leave worker</span></div>',
        unsafe_allow_html=True,
    )
    with st.expander("Try an example"):
        st.markdown("**Math:** What is the square of the average of 10 and 5?")
        st.markdown("**Leave balance:** How many leave days does Alice have?")
    question = st.text_area(
        "Your request",
        placeholder="Ask for a calculation or an employee leave balance…",
        height=112,
        label_visibility="collapsed",
        key="supervisor_worker_question_input",
    )
    submit = st.button(
        "✦  Delegate request",
        use_container_width=True,
        type="primary",
        key="supervisor_worker_submit",
    )
    if submit:
        if not question.strip():
            st.warning("Enter a request to get started.")
        else:
            with st.spinner("Supervisor is selecting a worker…"):
                try:
                    result = get_supervisor_worker_workflow().invoke({"query": question.strip()})
                    st.session_state.setdefault(history_key, []).append(
                        {
                            "question": question.strip(),
                            "worker": result.get("worker", "unknown"),
                            "expression": result.get("expression", ""),
                            "employee_name": result.get("employee_name", ""),
                            "answer": str(result.get("result", "No result was returned.")),
                        }
                    )
                except Exception as error:
                    st.error(
                        "The supervisor-worker workflow could not complete the request. "
                        f"Check OPENAI_API_KEY. Details: {error}"
                    )

    if st.session_state.get(history_key):
        st.markdown('<div class="section-label">Delegation history</div>', unsafe_allow_html=True)
        for message in st.session_state[history_key]:
            with st.chat_message("user"):
                st.markdown(message["question"])
            with st.chat_message("assistant"):
                worker_label = "Leave-balance worker" if message["worker"] == "leave" else "Math worker"
                st.caption(f"Supervisor delegated to · {worker_label}")
                if message["expression"]:
                    st.code(message["expression"], language="text")
                if message["employee_name"]:
                    st.caption(f"Employee · {message['employee_name']}")
                st.markdown(message["answer"])

st.divider()
st.caption("Powered by LangGraph · Configure OPENAI_API_KEY in .env to enable responses.")