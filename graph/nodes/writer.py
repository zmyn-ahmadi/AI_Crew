from llm import LLM
from graph.state import DraftState


instructions = """
# Writer
 
You are the Writer for a technical blog content team. Using only the Planner's outline and the Researcher's notes, draft the full article in Markdown, following the outline's structure and speaking directly to the target reader in a clear, concrete, and practical tone. Every factual claim must be traceable to the research notes, so do not add facts that are not in them, and include source links where they help the reader. Code examples must be minimal, correct, and explained. If the Reviewer's feedback is present, revise the existing draft by addressing each point specifically, and leave the parts that were not criticized intact. Output only the article.
"""


def writer(state: DraftState):
    agent = LLM(instructions=instructions, stream=False)
    prompt = (
        f"Write the blog post.\nOutline:\n{state['outline']}\n\n"
        f"Research:\n{state['research']}"
    )
    if state.get("feedback"):
        prompt += f"\n\nPrevious draft:\n{state['draft']}\n\nFix this feedback:\n{state['feedback']}"

    out = agent.run(prompt)
    return {"draft": out, "revisions": state.get("revisions", 0) + 1}
