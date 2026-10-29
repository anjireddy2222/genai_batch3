from fastapi import FastAPI
# from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp import Client
import httpx2


app = FastAPI()


# @app.post("/mcp-chat")
# async def mcp_chat():
#     # coonect t mcp server
#     # establish session
#     # use that session to get and run tools
#     tools = []
#     async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write, _):
#         print("mcp connected")
#         async with ClientSession(read, write) as session:
#             print("session created")
#             await session.initialze()
#             tools = await session.list_tools()


    
#     return { "tools": tools }


@app.get("/")
async def index_api():

    tools = []
    tool_result = ""
    tool_result2 = ""
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()

        tool_result = await client.call_tool("get_courses_list", {}) # (tool name and input data)
        tool_result2 = await client.call_tool("get_syllabus_demo_links", {})

    return { "data": tools, "result": tool_result, "result2": tool_result2 }


# token, api key, secret key

@app.get("/secured-mcp")
async def secured_mcp():

    # headers 
    # token = -> Authorization key -> Bearer token value
    # api key, secret, id -> company specified name as key -> value
    headers = {
        "Authorization": "Bearer kjsskasgf7851251298561fskjafbsajfagf5981651985bjkbaskjfbasgf95619825jkbjkbajc vbasfq856195625sjkabaskjgbaskg",
        "X-API-Key": "ghasgjkasask85693691165619861gjskajgaa"
    }
    # headers = {
    #     "X-API-Key": "ghasgjkasask85693691165619861gjskajgaa"
    # }
    tools = []
    async with httpx2.AsyncClient(headers=headers) as http_client:
        transport = streamable_http_client("http://127.0.0.1:8000/mcp", http_client=http_client)
        async with Client(transport) as client:
            tools = await client.list_tools()
            await client.call_tool("get_courses_list", {})


    




    return { "tools": tools }
