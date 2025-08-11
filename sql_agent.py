
import os
import urllib.parse
from phi.agent import Agent
from phi.tools.sql import SQLTools
from dotenv import load_dotenv
import urllib
# Load environment variables
load_dotenv()

# DEFINE THE DATABASE CREDENTIALS
db_user = os.getenv('DB_USER')
db_password = urllib.parse.quote_plus(os.getenv('DB_PSWD'))
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db_url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            db_user, db_password, db_host, db_port, db_name
        )
my_instructions=[
        "You are an assistant in Human Resources department with access to complete database schema.",
        "Read the human question and extract the answer from the database",
        "use like operator and '%' instead of equal to for matching literals"
        "Answer specific to the point, do not create or make up your own answers",
        "If the question is not relavant, respond I dont know."
    ]

gpt_instructions=[
    "You are an SQL Expert Agent with deep knowledge of the company’s relational database schema. Your job is to:",
        "- Convert user intent into optimized SQL queries.",
        "- Query the database to retrieve precise answers.",
        "- Always return results in a clean, human-readable table or summary.",
        "- Use only the available schema and data columns (employees, rates, availability, utilization %, projects, budgets, profitability, start/end dates, etc.).",
        "- Do not fabricate data. If the query is impossible with given schema, return a clear message.",
        "You handle queries like:",
        "- List available Java developers next month.",
        "- What’s the profitability of Project Phoenix?",
        "- Suggest a team for $50,000 budget for 2 months."
    ]

sql_agent = Agent(
    name="Database Reader",
    tools=[SQLTools(db_url=db_url)],
    instructions=gpt_instructions,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=False,
    prevent_hallucinations=True
)

def get_sql_response(query:str, API=False):
    if query is None:
        return "Please provide a question related to resume database"
    # elif user_session_id is None:
    #     return "Please provide userid"
    else:
        if API:
            # sql_agent.session_id = user_session_id
            structured_output = sql_agent.run(query, stream=False)
            # print(structured_output.messages[-1].content)
            return structured_output.messages[-1].content or "Sorry! couldn't get response from AI."
        else:
            sql_agent.print_response(query, stream=True)

# sql_agent.print_response("List the tables in the database. Tell me about contents of the users table")
# sql_agent.print_response("what is per hour rate of Rajender?")