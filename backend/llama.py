
"""
no need to setup vector db, extract/read files, embeddings conversion
folder -> 
pip install llama-index
pip install llama-index-llms-openai

"""
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class LlamaChatReq(BaseModel):
    user_msg: str




@app.post("/chat")
def llama_chat( req : LlamaChatReq ):

    documents = SimpleDirectoryReader("business_knowledge").load_data()

    # print( documents )

    index = VectorStoreIndex.from_documents(documents)

    # print(index)

    openai_llm = OpenAI(model="gpt-5.5")

    query_engine = index.as_query_engine(llm=openai_llm)

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
        8. dont imagine and give answers, if the data is not availbale in our business knowledge, connect with our team.
    
        User message: { req.user_msg }
    """

    ai_response = query_engine.query(prompt)

    return { "message": ai_response }





