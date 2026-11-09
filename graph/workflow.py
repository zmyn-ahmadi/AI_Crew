from langgraph.graph import StateGraph, START, END
from graph.nodes import supervisor, planner, researcher, writer, reviewer
from graph.state import DraftState
from graph.router import route_write


def build_graph():
    g = StateGraph(DraftState)
    g.add_node("supervisor", supervisor.supervisor)
    g.add_node("planner", planner.planner)
    g.add_node("researcher", researcher.researcher)
    g.add_node("writer", writer.writer)
    g.add_node("reviewer", reviewer.reviewer)

    g.add_edge(START, "planner")
    g.add_edge("planner", "researcher")
    g.add_edge("researcher", "writer")
    g.add_edge("writer", "reviewer")
    g.add_conditional_edges("reviewer", route_write, ["writer", "supervisor"])
    g.add_edge("supervisor", END)

    app = g.compile()
    return app
