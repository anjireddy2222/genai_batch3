
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv


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



@app.post("/chat")
def chat_func( req : ApiRequestData ):

    # print( req.conv_id )
    # print( req.user_message )

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

    User message: { req.user_message }
    """

    # general_prompt = f"""
    # You are AI assitant, answer user queries. 
    # User message: { req.user_message }
    # """

    openai_client = openai.OpenAI( api_key=os.getenv("OPENAI_API_KEY") )
    ai_response = openai_client.responses.create( model="gpt-5.5", input=prompt  )





    return { "message": "ok", "ai_response": ai_response }




"""
user message
get conversation history
get business knowledge
build prompt

send to ai

"""

