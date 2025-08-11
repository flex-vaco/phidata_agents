
from flask import Flask, request, session
from flask_session import Session
from flask_cors import CORS

import os, re
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from resume_agent_team import resume_team, get_response
from datetime import datetime
from sql_agent import get_sql_response

flask = Flask(__name__, static_folder="../docs")
flask.config["SESSION_PERMANENT"] = False
flask.config["SESSION_TYPE"] = "filesystem"
flask.secret_key = 'fract-secret-key'
Session(flask)
CORS(flask, supports_credentials=True)
chatHistoryLength = 3


validFileFormats  = [".pdf", ".doc", ".docx", "xls", "xlsx"]
docs_path = os.getenv("DOCS")

def getChatHistory():
    if session.get('chat_history'):
        return session['chat_history']
    else:
        return []

def setChatHistory(question, answer):
    chat_history = getChatHistory()
    if len(chat_history) > chatHistoryLength:
        chat_history.pop(0)
    
    chat_history.append({"Human": question, "AI":answer})
    session['chat_history'] = chat_history

def get_doc_list(category):
    doc_list = []
    for file in os.listdir(F'{docs_path}/{category}'):
        item={}
        if file.endswith(tuple(validFileFormats)):
            item['file_name'] = str(file)
            item['display_name'] = file.split(".")[0].replace("_"," ")
            item['file_path'] = F'{docs_path}/{category}/{str(file)}'
            doc_list.append(item)
    return doc_list

def isValidFileFormat(file_name):
    return file_name.endswith(tuple(validFileFormats))

import re
def remove_html_tags_regex(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@flask.route('/resume_query', methods = ['GET'])
def get_resume_agent_response():
    query = request.args.get("query", None)
    query = remove_html_tags_regex(query)
    user_session_id = request.args.get("user_id", None)
    if query is None or user_session_id is None:
        print("Please provide all the required params ")
        return "Please provide all the required params ", 400
    # resume_team.run(query, stream=False).messages[-1].content or "Sorry! couldn't get response from AI."
    ai_answer = get_response(query, user_session_id, API=True)
    return {"human_query":query, "ai_response": ai_answer}, 200

@flask.route('/sql_query', methods = ['GET'])
def get_sql_agent_response():
    query = request.args.get("query", None)
    query = remove_html_tags_regex(query)
    # user_session_id = request.args.get("user_id", None)
    if query is None:
        print("Please provide all the required params ")
        return "Please provide all the required params ", 400
    ai_answer = get_sql_response(query, API=True)
    return {"human_query":query, "ai_response": ai_answer}, 200

@flask.get("/health")
def get_health():
    """Check the health of the Api"""

    return {
        "status": "success",
        "router": "health",
        "path": "/health",
        "time": datetime.now(),
    }

# print(os.getenv("HTTP_HOST"), os.getenv("HTTP_PORT"), os.getenv("DEBUG_MODE"))
flask.run(host=os.getenv("HTTP_HOST"), port=os.getenv("HTTP_PORT"), debug=os.getenv("DEBUG_MODE"))
