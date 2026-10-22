from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_community.tools.file_management.read import ReadFileTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import json

load_dotenv()
app = FastAPI()

llm_client = ChatOpenAI(model = "gpt-5.5")
read_tool = ReadFileTool()
write_tool = WriteFileTool()

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
    "is_file_content_found": "",
    "is_read_operation": "yes or no",
    "is_write_operation": "yes or no"
    }}

    data:
    {req.msg}
    """
    print("llm 1 start")
    ai_response = llm_client.invoke(prompt)
    ai_response = json.loads(ai_response.content)
    print("llm 1 end")
    tool_result = ""

    if ai_response["is_read_operation"] == "yes":
        print("call read tool")
        tool_result = read_tool.run({ "file_path": ai_response["file_name"] })
        prompt = f"""
            analyse below content and explain what it is and use bullet point if required.
            data:
            {tool_result}
        """
        print("llm 2 start")
        ai_response = llm_client.invoke(prompt)
        ai_response = ai_response.content
        print("llm 2 end")
    elif ai_response["is_write_operation"] == "yes":
        print("call write tool")
        tool_result = write_tool.run({ "file_path": ai_response["file_name"],  "text": ai_response["file_content"], "append": False })

    

    



    return ai_response




