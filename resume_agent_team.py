from phi.agent import Agent
# from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.assistant import Assistant
from sql_agent import sql_agent as SQL_Agent
from vector_agent import vector_agent as RAG_Agent
from google_search_agent import google_search_agent as Internet_Search_Agent

from dotenv import load_dotenv
from rich.pretty import pprint 

load_dotenv()

my_model = OpenAIChat(id="gpt-4o")#Groq(id="llama-3.3-70b-versatile")
my_instructions = [
        "You are an assistant in Human Resources department with access to database schema and knowledge base of resumes",
        "First, search for the answer in the database with sql_agent tool.",
        "Then, if sql_agent answer is not satisfactory, ask the vector_agent to read knowledge base to get more information.",
        "Respond specific to the point, do not create or make up your own answers. Do not relay errors to output.",
        "If you cannot get answer from sql_agent and/or vector_agent though the question is related to resumes and employment use google_search_agent to find answer from internet",
        "Respond politely that you cannot answer it."
    ]

gpt_instructions = [
        "You are the Master Orchestrator Agent for a Resource Intelligence System, assisting on queries from Human Resources department.",
        """You have access to three specialized agents:
        1. SQL_Agent — queries structured business data in the company’s relational database (employee_details, availability, employee_project_allocations, employee_project_utilization, budgets, profitability).
        2. RAG_Agent — retrieves and ranks results from a vector database of employee resumes, skills, and unstructured documents.
        3. Internet_Search_Agent — finds fresh, external, or unknown information from the web.""",
        """Your responsibilities:
        Understand the user’s intent.
        Identify which agent(s) to invoke.
        If the question is answerable entirely from structured company data → use SQL Agent.
        If the question is about skills, expertise, or semantic matches from resumes → use RAG Agent.
        If the question needs fresh external information → use Internet Search Agent.
        If multiple agents are needed, call them in sequence and merge results.
        Always produce a clear, concise, and context-aware final answer for the user.
        If the user’s query is ambiguous, ask clarifying questions before invoking agents."""
    ]

resume_team = Agent(
    name="HR Query Responder Team",
    team=[SQL_Agent, RAG_Agent, Internet_Search_Agent],
    model=my_model,
    instructions=gpt_instructions,
    show_tool_calls=False,
    markdown=True,
    prevent_hallucinations=True,
    prevent_prompt_leakage=True,
    read_chat_history=True,
    add_history_to_messages=True,
    num_history_responses=3,
)

def get_response(query:str, user_session_id:str, API=False):
    if query is None:
        return "Please provide a question related to resume database"
    elif user_session_id is None:
        return "Please provide userid"
    else:
        if API:
            resume_team.session_id = user_session_id
            structured_output = resume_team.run(query, stream=False)
            # print(structured_output.messages[-1].content)
            return structured_output.messages[-1].content or "Sorry! couldn't get response from AI."
        else:
            resume_team.print_response(query, stream=True)


# q = "We have a total budget of 100 dollars per hour to build a Netsuite team. Feel free to suggest a team of resources with netsuite skills who can fit into this budget. The sum of rates of these resources should not exceed the budget."
# get_response(query=q, API=False)
# get_response(query="what is per hour rate of Rajender? Also get his profile summary.", API=False)
# get_response(query="List people with SalesForce skills with hourly rate under $45, also make sure they have expereince working with Vaco", API=False)
