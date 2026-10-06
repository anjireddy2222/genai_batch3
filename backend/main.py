
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import pymysql


app = FastAPI()
load_dotenv()

# Path -> http method -> python method -> response return

class ApiRequestData(BaseModel):
    user_message: str
    conv_id: int

class LoginAPiData(BaseModel):
    email: str
    password: str


@app.post("/login")
def login_func( req : LoginAPiData ):

    return 'login success'

def get_db_connection():
    return pymysql.connect( host="localhost", user="root", password="15081947", port=3307 , database="sales_db", cursorclass=pymysql.cursors.DictCursor ) # 3306

@app.post("/chat")
def chat_func( req : ApiRequestData ):

    # print( req.conv_id )
    # print( req.user_message )

    db_con = get_db_connection()
    db_cursor = db_con.cursor()
    sql_query = "select * from conv_messages where conv_id = %s  ;"
    db_cursor.execute(sql_query, (req.conv_id))
    history_data = db_cursor.fetchall()
    history_for_ai = ""
    for message in history_data:
        # print(message)
        history_for_ai = history_for_ai + f"role:{message["message_from"]} and content: {message["message"]}\n"
    # print(history_for_ai)



    prompt = f""" 
    you are AI sales assistant for softwareschool. we are providing coding classes in telugu. 

    You help students to choose right course based on thei background and expereince, answer their questions, and guide them to choose right course.

    Rules & Instructions

    1. keep responses short 3 to 6 lines only
    2. use friendly and professional language
    3. use simple english and always reply in english only
    4. ask 1 or 2 questions ata a time
    5. if you don't know the answer, please escalate o human support
    6. if user is agressive, connect to human
    7. never promise job guarantee

    Course 1:
    name: GenAI, AI engineer
    type: live classes
    timings: 8PM IST monday to Friday
    Duration: 3 months
    Syllabus: https://genai-syllabus-link
    Demo: https://genai-demo-link
    technologies: Python, mysql, prompt engineering, genai, llms, agent

    Course 1:
    name: ReactJS
    type: Recorded classes
    Syllabus: https://reactjs-syllabus-link
    Demo: https://reactjs-demo-link
    technologies: html, css, bootstrap, js, typescript, reactjs, prokects, github

    Conversation history:
    {history_for_ai}

    User message: { req.user_message }
    """

    # general_prompt = f"""
    # You are AI assitant, answer user queries. 
    # User message: { req.user_message }
    # """

    openai_client = openai.OpenAI( api_key=os.getenv("OPENAI_API_KEY") )
    ai_response = openai_client.responses.create( model="gpt-5.5", input=prompt  )


    # store history -> user message and ai reply
    insert_query = "insert into conv_messages(message, message_from, conv_id) values(%s, %s, %s);"
    db_cursor.execute(insert_query, (req.user_message, "user", req.conv_id))

    insert_query = "insert into conv_messages(message, message_from, conv_id) values(%s, %s, %s);"
    db_cursor.execute( insert_query, (ai_response.output_text, "assistant", req.conv_id ) )

    db_con.commit( )
    
    db_con.close( )




    return { "message": "ok", "ai_response": ai_response.output_text }




"""
user message
get conversation history
get business knowledge
build prompt

send to ai

"""

