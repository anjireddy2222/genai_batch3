from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from prompts.interview_template import interview_prompt_template
import json
import pymysql
from langchain.tools import tool
from tools.interview_tools import send_email, create_offer_letter

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
    interview_id: str
    user_id: str
    user_message: str

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


def get_db_connection():
    return pymysql.connect(host="localhost", database="interview_db", password="15081947", user="root", port=3307, cursorclass=pymysql.cursors.DictCursor)


@app.post("/chat")
def lc_chat( req : InterviewInputData ):

    db_con = get_db_connection()
    db_cursor = db_con.cursor()
    # get interview details
    get_query = "select * from interview_details where interview_id = %s and user_id = %s ;"
    db_cursor.execute(get_query, ( req.interview_id, req.user_id  ))
    interview_details = db_cursor.fetchall()
    experience = ""
    technologies = ""
    country = ""
    for row in interview_details:
        experience = row["exp"]
        technologies = row["technologies"]
        country = row["country"]

    # save user message
    # insert_query = "insert into interview_chats(interview_id, user_id, message, msg_role) values(%s,%s,%s,%s )"
    # db_cursor.execute(insert_query, ( req.interview_id, req.user_id, req.user_message, "user" ))
    # db_con.commit()

    # get interview history
    get_query = "select * from interview_chats where interview_id = %s and user_id = %s ;"
    db_cursor.execute(get_query, (req.interview_id, req.user_id))
    history_details = db_cursor.fetchall()
    history = ""
    for row in history_details:
        history = history + f"role: {row["msg_role"]} and content: {row["message"]} "


    template = PromptTemplate.from_template(interview_prompt_template)
    prompt = template.format( exp=experience, technologies=technologies, country=country, history=history )

    llm_client = ChatOpenAI(model="gpt-5.5")
    # llm_client = llm_client.with_structured_output(InterViewResponse)
    llm_client = llm_client.bind_tools( [ send_email, create_offer_letter  ] )
    response = llm_client.invoke(prompt)

    if len(response.tool_calls) > 0 :
        print("tools calling")

        for tool in response.tool_calls:
            if tool["name"] == "send_email":
                print("send_email tool calling")
                send_email.invoke(tool["args"])

            if tool["name"] == "create_offer_letter":
                print("create_offer_letter tool calling")
                create_offer_letter.invoke(tool["args"])

    # db_cursor.execute(insert_query, (req.interview_id, req.user_id, response.next_question, "assistant"  ))
    # db_con.commit()



    

    return response



