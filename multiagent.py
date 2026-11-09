from graph import workflow
from rich.console import Console
from rich.markdown import Markdown

console = Console()

app = workflow.build_graph()

while True:
    topic = input("\nTopic: \n")
    result = app.invoke({"topic": topic, "revisions": 0})
    console.print("\n\n", Markdown(result["draft"]))
