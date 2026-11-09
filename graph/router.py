from graph.state import DraftState


def route_write(state: DraftState):
    if state["score"] >= 8 or state["revisions"] >= 3:
        return "supervisor"
    return "writer"
