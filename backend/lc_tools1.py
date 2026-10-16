"""
pip install langchain-community

important

internet search
API calling 
DB tool
File handling

"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")

internet_search_tool = DuckDuckGoSearchRun()

results = internet_search_tool.run("openai ipo")

print( results )

prompt = f"""
summerize and give me data in bullet points
data:
{results}
"""

ai_reponse = llm_client.invoke(prompt)

print(ai_reponse.content)


