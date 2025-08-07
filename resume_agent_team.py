from phi.agent import Agent
# from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.assistant import Assistant
from sql_agent import sql_agent
from vector_agent import vector_agent
from google_search_agent import google_search_agent

from dotenv import load_dotenv
from rich.pretty import pprint 

# Load environment variables
load_dotenv()

my_model = OpenAIChat(id="gpt-4o")#Groq(id="llama-3.3-70b-versatile")

resume_team = Agent(
    name="Resume Responder Team",
    team=[sql_agent, vector_agent, google_search_agent],
    model=my_model,
    instructions=[
        "You are an assistant in Human Resources department with access to database schema and knowledge base of resumes",
        "First, search for the answer in the database with sql_agent tool.",
        "Then, if sql_agent answer is not satisfactory, ask the vector_agent to read knowledge base to get more information.",
        "Respond specific to the point, do not create or make up your own answers. Do not relay errors to output.",
        "If you cannot get answer from sql_agent and/or vector_agent though the question is related to resumes and employment use google_search_agent to find answer from internet",
        "Respond politely that you cannot answer it."
    ],
    show_tool_calls=False,
    markdown=True,
    prevent_hallucinations=True,
    prevent_prompt_leakage=True,
    read_chat_history=True
)

def get_response(query:str, API=False):
    if query is None:
        return "Please provide a question related to resume database"
    else:
        if API:
            structured_output = resume_team.run(query, stream=False)
            print(structured_output.messages[-1].content)
            return structured_output.messages[-1].content
        else:
            # resume_team.print_response("List all people with Java skills", stream=True)
            resume_team.print_response(query, stream=True)
            # structured_op = resume_team.run(f"List all people with python skills", stream=False)
            # pprint(structured_op.messages[-1].content)
            # print(structured_op.messages[-1].content)

#get_response(query="what is per hour rate of Rajender? Also get his profile summary. get 2 references from his Linkedin proflie", API=False)
# get_response(query="List people with SalesForce skills with hourly rate under $45, also make sure they have expereince working with Vaco", API=False)

# get_response(query="1. List people with Java Skils. " \
# "2. Select a random name from the list and give the profile summary. " \
# "3. Give me 5 questions to ask him/her based on the summary.", API=False)

# get_response(query="1. List people with React Skils. " \
# "2. Select a random name from the list and give the profile summary. " \
# "3. Get the average salary for the above profile in current market.", API=False)