# fastapi django flask
# fastapi

from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()


# login
# path, method -> 
# http://127.0.0.1:8000/auth/login

@app.post("/auth/login")
def login():
    print("login success")

    return { "result": "sucess", "message": "login success", "data": { "user_id": 1, "token": "asgasgasgasgasg" } }


@app.get("/get-user-data")
def get_data():

    return { "user_id": 1, "token": "asgasgasgasgasg" }

class InputData(BaseModel):
    user_message: str
    user_id: int


@app.post("/chat")
def chat( req : InputData ):

    openai_client = openai.OpenAI( api_key = "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" )

    prompt = """
    you are AI sales assistant for softwareschool. we are providing coding classes in telugu. 

    Course
    """

    ai_response = openai_client.responses.create( model="gpt-5.5", input=req.user_message )

    ai_response = ai_response.output_text



    return { "result": "success", "data": ai_response }

