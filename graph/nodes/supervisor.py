import re

from graph.state import DraftState
from tools.tools import write_file


def supervisor(state: DraftState):
    """Save the final draft to data/<topic-slug>.md."""
    slug = re.sub(r"[^a-z0-9]+", "-", state["topic"].lower()).strip("-") or "draft"
    path = f"{slug}.md"
    write_file(path, state["draft"])
    return {"path": path}
