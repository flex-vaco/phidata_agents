from phi.agent import Agent
from knowledge_base import pdf_knowledge_base

vector_agent = Agent(
    name="Vector Reader",
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    instructions=[
        "You are an assistant in Human Resources department with access to a knowledge base of resumes",
        "Read the human question and extract the answer from the knowledge base of resumes",
        "Respond specific to the point, do not create or make up your own answers",
        "If the question is not related to resumes and employment, respond I dont know."
    ],
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=False,
    markdown=True,
    prevent_hallucinations=True,
)
# vector_agent.knowledge.load(recreate=False)

# vector_agent.print_response("List people with React skills", stream=True)
# vector_agent.print_response("How to travel to Mars from India?")
# vector_agent.print_response("from above people, select a person who can be more effective for client interaction role", stream=True)