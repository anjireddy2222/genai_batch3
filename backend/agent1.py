from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import BaseModel
from langchain.tools import tool
import middlware as md
from langchain.agents.middleware import ModelRetryMiddleware, ModelFallbackMiddleware, ToolRetryMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware

load_dotenv()

app = FastAPI()

"""
llm
tools
prompt
rag
conversation history
middlewares
"""

prompt = f"""
you are helpful AI sales agent for softwareschool, people will message youto enquire about our courses, syllabys and demos.please ask about their background, goals and suggest best suitable courses.

ReactJS course:
technologies: html, css, bootstrap, js, reactjs, aws, git and github
mode: recorded

Springboot course:
technolgies: java, mysql, springboot, microservices, redis, kafka, docker, aws, git and github
mode: recorded

GenAI course:
technologies: python, llm, prompt engineeering, genai, langchain, rag, langraph
mode: live

"""

@tool(description="use this tool to get reactjs syllabus link")
def get_reactjs_syllabus():
    return "https://reactjs-syllabus.com"

@tool(description="use this tool to get java springboot syllabus")
def get_spring_syllabus():
    return "https://spring-syllabus.com"

@tool(description="use this tool to get genai syllabus link")
def get_genai_syllabus():
    # raise Exception("Genai course syllabus tool is down, please retyr after sometime.")
    return "http://genai-syllabus.com"


@tool(description="use this tool to get course name based on course id")
def get_course_name(course_id: str):

    if course_id == "1":
        return "ReactJS"
    
    if course_id == "2":
        return "Springboot"
    
    if course_id == "3":
        return "GenAI"

    return f"We dont have any course related to id {course_id}"



tools = [ get_genai_syllabus, get_reactjs_syllabus, get_spring_syllabus, get_course_name ]





class ChatRequest(BaseModel):
    msg: str


class AIResponse(BaseModel):
    interested_course: str
    ai_reply: str
    user_email: str
    user_mobile: str


agent = create_agent("openai:gptanji-5647524.5", 
                     system_prompt=prompt, 
                     tools=tools, 
                     response_format=AIResponse, 
                     name="ss_sales_agent", 
                     middleware=[
                         md.LoggingMiddleware(),
                         ModelRetryMiddleware(max_retries=4, max_delay=10),
                         ModelFallbackMiddleware("openai:gpt-5.5"),
                         ToolRetryMiddleware(max_retries=4, max_delay=10),
                         ToolCallLimitMiddleware(run_limit=20, tool_name="get_course_name", exit_behavior="error"),
                         ModelCallLimitMiddleware(run_limit=10, exit_behavior="error")
                     ]
                     )


@app.post("/chat")
def chat( req: ChatRequest):
    response = ""
    try:


        input_data = {
            "messages": [
                { "role": "user", "content": req.msg }
            ]
        }


        agent_reuslt = agent.invoke( input_data )
        # send user message to ai
        # tool calls detected and return to backend code
        # execute tools
        # send tool reults to ai
        # generate response 
        # agent_reuslt["structured_response"]




        return { "data": agent_reuslt }
    
    except Exception as e:
        print(f"###\n Exception {e}")
        response = str(e)

    return response

