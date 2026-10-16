from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import RequestsGetTool
from langchain_community.utilities.requests import TextRequestsWrapper

"""
URL/API End point: http://softwareschool.co/api/login
Method: GET/POST/DELETE
Headers
Data: 
"""

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

api_wrapper = TextRequestsWrapper()

api_tool = RequestsGetTool( requests_wrapper=api_wrapper, allow_dangerous_requests=True )

api_results = api_tool.run("https://dummyjson.com/products")

print( api_results )

prompt = f"""

is there any dog food products. filter and give me data in json format

data
{api_results}
"""

ai_response = llm_client.invoke(prompt)

print(ai_response.content)



