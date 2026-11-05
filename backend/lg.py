from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# state

class PasswordResetState(TypedDict):
    email: str
    is_email_exists: bool
    reset_link_url: str
    is_email_sent: bool
    task_status: bool
    message: str

class CustomerSupportState(TypedDict):
    email: str
    mobile: str
    order_id: str
    enquiry: str
    ticket_id: int
    ticket_status: str
    ticket_date: str
    comments: str

# nodes
def collect_email(state):
    state["email"] = "contact@ss.co"
    print(f"inside collect_email node: {state}")
    return state

def check_email_in_db(state):
    state["is_email_exists"] = False
    print(f"inside check_email_in_db node: {state}")
    return state

def generate_link(state):
    state["reset_link_url"] = "https://reste-link.com"
    print(f"inside generate_link node: {state}")
    return state

def send_email(state):
    if state["is_email_exists"] == True:
        print("sent email")
        state["is_email_sent"] = True
        state["message"] = "Your password reste link sent to your email id"
    else:
        state["message"] ="We dont have any account with your email id."

    print(f"inside send_email node: {state}")
    return state

def show_message(state):
    print(f"inside show_message node: {state}")
    print(state["message"])
    return state

graph_builder = StateGraph(PasswordResetState)

# add nodes
graph_builder.add_node("generate_link_node", generate_link)
graph_builder.add_node("send_email_node", send_email)
graph_builder.add_node("collect_email_node", collect_email )
graph_builder.add_node('check_email_in_db_node', check_email_in_db)
graph_builder.add_node("show_message_node", show_message)

# add edges
graph_builder.add_edge(START, "collect_email_node")
graph_builder.add_edge("collect_email_node", "check_email_in_db_node")
graph_builder.add_edge("check_email_in_db_node", "generate_link_node")
graph_builder.add_edge("generate_link_node", "send_email_node")
graph_builder.add_edge("send_email_node", "show_message_node")
graph_builder.add_edge("show_message_node", END)


agent = graph_builder.compile()

result = agent.invoke({"email":"", "is_email_exists": None, "reset_link_url":"", "is_email_sent": None, "task_status": None, "message": ""})

print(f"\n####\n {result}")


