from fastapi import FastAPI
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

app = FastAPI()


# interview
# node 1: generate offer letter 
# conditiona route -> check approval status
# node 3 -> if approved -> send offer letter -> end
# node 4 -> if rejected -> send rejection emaill -> end


class CandidateData(TypedDict):
    name: str
    email: str
    approval_status: str
    message: str

def approval(state):
    print("approval node started")
    res = interrupt("HR approval required, Please check candidate interview details and approve or reject the candidate")
    state["approval_status"] = res
    print(f"\n {res} \n")

    return state
    
def generate_offer_letter(state):
    print("offer letter generated")
    return state

def send_offer_letter(state):
    print(f"offer letter sent to {state["email"]} ")
    return state

def send_rejection_email(state):
    print(f"rejection email sent to {state["email"]}")
    return state

# conditional route
def check_approval_status(state):
    if state["approval_status"] == "approved":
        return "yes"
    else:
        return "no"

graph_builder = StateGraph(CandidateData)

graph_builder.add_node("approval_node", approval)
graph_builder.add_node("generate_offer_letter_node", generate_offer_letter)
graph_builder.add_node("send_offer_letter_node", send_offer_letter)
graph_builder.add_node("send_rejection_email_node", send_rejection_email)

graph_builder.add_edge(START, "generate_offer_letter_node")
graph_builder.add_edge("generate_offer_letter_node", "approval_node")
graph_builder.add_conditional_edges("approval_node", check_approval_status, { "yes": "send_offer_letter_node", "no": "send_rejection_email_node"  } )
graph_builder.add_edge("send_offer_letter_node", END)
graph_builder.add_edge("send_rejection_email_node", END)

thread_memeory = MemorySaver()

agent = graph_builder.compile(checkpointer=thread_memeory)

result1 = agent.invoke({ "approval_status": "", "name": "anji reddy", "email": "ss@ss.co", "message": "ok"  }, { "configurable": { "thread_id": "interview_id_1" } })
result2 = agent.invoke({ "approval_status": "", "name": "dd", "email": "dd@ss.co", "message": "ok"  }, { "configurable": { "thread_id": "interview_id_2" } })

# result1_1 = agent.invoke(Command(resume="reject"), { "configurable": { "thread_id": "interview_id_1" } })
# result2_1 = agent.invoke(Command(resume="approved"), { "configurable": { "thread_id": "interview_id_2" } })

# print("#### start 1")
# print(result1)
# print("\n##")
# print(result1_1)
# print("\n#### start 2")
# print(result2)
# print("\n##")
# print(result2_1)

class ApprovalRequest(BaseModel):
    approval_status: str
    thread_id: str

@app.post("/approval")
def approval_api(req : ApprovalRequest):
    res = agent.invoke(Command(resume=req.approval_status), { "configurable": { "thread_id": req.thread_id } })
    return res
