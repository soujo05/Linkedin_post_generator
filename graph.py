from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.writer_agent import writer_agent


# -----------------------------
# Define the shared state schema
# -----------------------------
class AgentState(TypedDict, total=False):
    topic: str
    tone: str
    length: str
    research: str
    summary: str
    post: str


# -----------------------------
# Build the LangGraph workflow
# -----------------------------
def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes (functions/agents)
    graph.add_node("research_node", research_agent)
    graph.add_node("summarizer_node", summarizer_agent)
    graph.add_node("writer_node", writer_agent)

    # Define edges (execution order)
    graph.add_edge(START, "research_node")
    graph.add_edge("research_node", "summarizer_node")
    graph.add_edge("summarizer_node", "writer_node")
    graph.add_edge("writer_node", END)

    # Compile graph into executable app
    app = graph.compile()
    return app


# -----------------------------
# Run the full agent pipeline
# -----------------------------
def run_pipeline(topic: str, tone: str, length: str):
    """
    Runs the full 3-step pipeline (research → summarize → write)
    and returns both the final state and a mermaid visualization.
    """
    # Build the graph
    app = build_graph()

    # Initialize state
    state = {
        "topic": topic,
        "tone": tone,
        "length": length
    }

    # Run the graph synchronously
    final_state = app.invoke(state)

    # Generate mermaid visualization of the workflow
    mermaid_graph = app.get_graph(xray=True).draw_mermaid()

    return final_state, mermaid_graph
