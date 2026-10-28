from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from fastapi import FastAPI
from pydantic import BaseModel
from sql import sql_schema
import json

load_dotenv()

app = FastAPI()

llm_client = ChatOpenAI(model="gpt-5.5")

# mysql+pymysql://user_name:password@server_host:port_number/db_name
db_con = SQLDatabase.from_uri("mysql+pymysql://root:15081947@localhost:3307/amazon_db")
db_tool = QuerySQLDataBaseTool(db=db_con)

class ChatRequest(BaseModel):
    msg: str
    chart_type: str

@app.post("/db-chat")
def db_chat( req : ChatRequest ):
    # 
    sql_prompt = f"""
    You are SQL expert. Generate sql query based on user message.
    SQL Schema:
    {sql_schema}

    User message: {req.msg}

    always return response in JSON format only, dont put it inside code block or quotes
    {{
        "sql_query": "",
        "sql_query_generated": "yes or no"
    }}
    """
    ai_sql_response = llm_client.invoke(sql_prompt)
    ai_sql_response = json.loads(ai_sql_response.content)

    db_results = db_tool.run(ai_sql_response["sql_query"])

    summary_prompt = f"""
    user question: {req.msg}
    database results: { db_results }
    generate helpful summary based on user message and db results.
    always return response in JSON format only. dont put results inside code block or quotes.
    {{
        "ai_response": "summary"
    }}
    """

    ai_summary = llm_client.invoke(summary_prompt)
    ai_summary = json.loads(ai_summary.content)



    return { "data": ai_summary }

