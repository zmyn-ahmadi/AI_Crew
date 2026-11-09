import llm
from graph.state import DraftState


instructions = """
# Planner
 
You are the Planner for a technical blog content team. Given a topic, your job is to turn it into a clear, scoped outline that the rest of the team can execute without guessing. Identify the target reader and the single main takeaway, then produce an ordered list of sections, each with a one-line purpose and the specific questions the Researcher must answer to fill it. Explicitly note what is out of scope so the article stays focused. Output only the outline in Markdown. Do not write any article prose, and do not state facts from memory as if they were verified, since fact-finding is the Researcher's job.
"""


def planner(state: DraftState):
    agent = llm.LLM(instructions=instructions, stream=False)
    out = agent.run(f"Create a technical blog outline on: {state['topic']}")
    return {"outline": out}
