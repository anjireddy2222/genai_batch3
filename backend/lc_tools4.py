from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_community.tools.file_management.read import ReadFileTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

llm_client = ChatOpenAI(model = "gpt-5.5")

class InputData(BaseModel):
    msg: str


@app.post("/files-chat")
def files_chat( req : InputData ):

    prompt = f"""
    extract file name and content from below data and return it in json format only, 

    {{
    "file_name": "",
    "file_content": "",
    "is_filename_found": "",
    "is_file_content_found": ""
    }}

    data:
    {req.msg}
    """

    ai_response = llm_client.invoke(prompt)



    return ai_response.content




