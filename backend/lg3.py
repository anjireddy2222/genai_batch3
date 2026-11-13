from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import TypedDict
from pydantic import BaseModel
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")


class ChatState(TypedDict):
    user_message: str
    ai_reply: str


def chat_node(state):
    print("calling llm")
    response = llm_client.invoke(input=state["user_message"])
    state["ai_reply"] = response.content

    return state

graph_builder = StateGraph(ChatState)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)


workflow = graph_builder.compile()



# print( result )

app = FastAPI()

class ChatRequest(BaseModel):
    msg: str


@app.post("/chat")
def chat( req : ChatRequest ):

    result = workflow.invoke({ "ai_reply": "", "user_message": req.msg})

    return result

@tool(description="use this tool to get available courses in softwareschool")
def ss_tool():
    return """
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

ai_agent = create_agent(model=llm_client, tools=[ss_tool], system_prompt="you are ai sales agent for softwareschool, we are providng coding classes in telugu, undertsnad user background, goals and suggest best courses")

def agent_chat_node(state):
    print("agent running inside workflow node")
    response = ai_agent.invoke({"messages": state["user_message"]})
    state["ai_reply"] = response
    print(response)

    return state

graph_builder2 = StateGraph(ChatState)
graph_builder2.add_node("agent_chat_node", agent_chat_node)
graph_builder2.add_edge(START, "agent_chat_node")
graph_builder2.add_edge("agent_chat_node", END)

workflow2 = graph_builder2.compile()


@app.post("/agent-chat")
def agent_chat( req : ChatRequest ):
    response = workflow2.invoke({"user_message": req.msg, "ai_reply": ""})

    return response




