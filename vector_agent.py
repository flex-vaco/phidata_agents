from phi.agent import Agent
from knowledge_base import pdf_knowledge_base
my_instructions =[
        "You are an assistant in Human Resources department with access to a knowledge base of resumes",
        "Note that the file-names are not actual names of persons, however the file content has a person name, use person name in your answers",
        "Read the human question and extract the answer from the knowledge base of resumes",
        "Respond specific to the point, do not create or make up your own answers",
        "If the question is not related to resumes and employment, respond I dont know."
    ]

gpt_instructions = [
    "You are a Resume and Skills Intelligence Agent.",
    """You retrieve information from a vector database of employee resumes, certifications, and unstructured documents.
    Your tasks:
    Find employees with relevant skills, experience, or projects.
    Rank and return the best matches based on semantic similarity.
    Include brief summaries from the retrieved documents that justify the match.
    When relevant, combine your output with structured data from the SQL Agent if requested by Master Agent.
    You handle queries like:
    - Find machine learning engineers with NLP experience.
    - Who has worked on AWS migration?
    - Suggest senior .NET developers with at least 10 years’ experience."""
]
vector_agent = Agent(
    name="Vector Reader",
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    instructions=gpt_instructions,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=False,
    markdown=True,
    prevent_hallucinations=True,
)
# vector_agent.knowledge.load(recreate=False)

# vector_agent.print_response("List people with 5 years expereince in React JS at a competitive rate compared to current market trends", stream=True)
# vector_agent.print_response("How to travel to Mars from India?")
# vector_agent.print_response("from above people, select a person who can be more effective for client interaction role", stream=True)