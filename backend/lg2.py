from fastapi import FastAPI
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END




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

graph_builder.add_node("generate_offer_letter_node", generate_offer_letter)
graph_builder.add_node("send_offer_letter_node", send_offer_letter)
graph_builder.add_node("send_rejection_email_node", send_rejection_email)

graph_builder.add_edge(START, "generate_offer_letter_node")
graph_builder.add_conditional_edges("generate_offer_letter_node", check_approval_status, { "yes": "send_offer_letter_node", "no": "send_rejection_email_node"  } )
graph_builder.add_edge("send_offer_letter_node", END)
graph_builder.add_edge("send_rejection_email_node", END)

agent = graph_builder.compile()

result = agent.invoke({ "approval_status": "rejected", "name": "anji reddy", "email": "ss@ss.co", "message": "ok"  })


print(result )

