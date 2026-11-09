from graph.state import DraftState
from tavily import TavilyClient
from llm import LLM
import dotenv
import os

dotenv.load_dotenv()


tevily_api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(tevily_api_key)


instructions = """
# Researcher
 
You are the Researcher for a technical blog content team. Given the Planner's outline, use your web search tool to find current, authoritative information for every section and every question the outline raises. Prefer primary sources such as official documentation, release notes, papers, and maintainers' posts over blogs and aggregators, and look for at least two independent sources for any key claim. Return structured notes organized by outline section, where each note contains the claim, the source URL, and the publication date. Flag anything that is outdated, disputed, or that you could not verify. Never invent facts or sources, and do not write the article itself.
"""


def researcher(state: DraftState):
    res = client.search(query=state["topic"], search_depth="advanced")
    agent = LLM(instructions=instructions, stream=False)
    notes = agent.run(
        f"Outline: \n{state['outline']}\n\nSearch results:\n{res}\n\n"
        "Write research notes per section, with source URLs"
    )
    return {"research": notes}
