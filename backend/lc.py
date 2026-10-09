from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from prompts.interview_template import interview_prompt_template
import json

load_dotenv()

app = FastAPI()

"""
AI -> interview candidate based on user profile and and send email

INput:
technologies, exp, country

Recieve input and send to AI

complete interview process

if selected send offer letter -> email

"""


class InterviewInputData(BaseModel):
    name: str
    experience: str
    technologies: str
    country: str
    ai_question: str
    user_answer: str

class InterViewResponse(BaseModel):
    next_question: str
    current_question_overall_rating: int
    current_question_technical_rating: int
    current_question_communication_rating: int
    overall_rating: int
    ovrall_technical_rating: int
    overall_communication_rating: int
    is_interview_completed: str
    final_interview_result: str


@app.post("/chat")
def lc_chat( req : InterviewInputData ):

    template = PromptTemplate.from_template(interview_prompt_template)
    prompt = template.format( name=req.name, exp=req.experience, technologies=req.technologies, country=req.country, history="", question=req.ai_question, user_answer=req.user_answer )

    llm_client = ChatOpenAI(model="gpt-5.5")
    llm_client = llm_client.with_structured_output(InterViewResponse)
    response = llm_client.invoke(prompt)

    

    return response



