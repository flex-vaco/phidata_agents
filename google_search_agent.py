from phi.agent import Agent
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from rich.pretty import pprint 

# Load environment variables
load_dotenv()
my_instructions=[
        "Given a topic by the user, search for 10 relevant items on internet and select the top 4 unique items."
        "Summarize the content from top 4 unique items and respond in English only",
        "Cite the information sources as weblinks at the end."
]

gpt_instructions=[
    "You are an External Knowledge & Web Search Agent.",
    """Your job:
    Search the internet for real-time or unknown data not in company databases.
    Summarize key points from credible sources.
    Provide links to original sources when possible.
    Avoid returning outdated or irrelevant results.
    You handle queries like:
    - What are the average hourly rates for cloud architects in the US?
    - Latest Java LTS version and its features.
    - Market trends in AI developer salaries in 2025."""
]

google_search_agent = Agent(
    tools=[GoogleSearch()],
    description="You are a search agent that helps users find the information from internet.",
    instructions=gpt_instructions,
    show_tool_calls=False,
)
# op = google_search_agent.run("React interview questions for 10 years experienced", markdown=False).messages[-1].content
# pprint(op)