from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()




@app.post("/chat")
def lc_chat():
    llm_client = ChatOpenAI(model="gpt-5.5")


    response = llm_client.invoke("explain about RAG")

    return response.content



