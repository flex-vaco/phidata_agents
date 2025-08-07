
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

sql_agent = Agent(
    name="Database Reader",
    tools=[SQLTools(db_url=db_url)],
    instructions=[
        "You are an assistant in Human Resources department with access to complete database schema.",
        "Read the human question and extract the answer from the database",
        "use like operator and '%' instead of equal to for matching literals"
        "Answer specific to the point, do not create or make up your own answers",
        "If the question is not relavant, respond I dont know."
    ],
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=False,
    prevent_hallucinations=True
)
# sql_agent.print_response("List the tables in the database. Tell me about contents of the users table")
# sql_agent.print_response("what is per hour rate of Rajender?")