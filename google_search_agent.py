from phi.agent import Agent
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from rich.pretty import pprint 

# Load environment variables
load_dotenv()

google_search_agent = Agent(
    tools=[GoogleSearch()],
    description="You are a search agent that helps users find the information from internet.",
    instructions=[
        "Given a topic by the user, search for 10 relevant items on internet and select the top 4 unique items."
        "Summarize the content from top 4 unique items and respond in English only",
        "Cite the information sources as weblinks at the end."
    ],
    show_tool_calls=False,
)
# op = google_search_agent.run("React interview questions for 10 years experienced", markdown=False).messages[-1].content
# pprint(op)