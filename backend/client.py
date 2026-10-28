from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


app = FastAPI()


@app.post("/mcp-chat")
async def mcp_chat():
    # coonect t mcp server
    # establish session
    # use that session to get and run tools
    tools = []
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        print("mcp connected")
        async with ClientSession(read, write) as session:
            print("session created")
            await session.initialze()
            tools = await session.list_tools()


    
    return { "tools": tools }




