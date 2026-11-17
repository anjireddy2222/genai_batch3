from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM


load_dotenv()

llm_client = LLM(model="gpt-5.5")

# research -> article

research_agent = Agent(role="Online content researcher", goal="find latest ai news and trends", backstory="", llm=llm_client)

writer_agent = Agent(role="Content writer", goal="wrte professional LinkedIn articles based on the data collected by research_agent", backstory="", llm=llm_client)

research_task = Task(description="research latest ai news", agent=research_agent, expected_output="summary of latest ai news and trends and important updates")
writing_task = Task(description="write linkedin article", agent = writer_agent, expected_output="a weel structured professional LinkedIn article")

workflow = Crew(agents=[research_agent, writer_agent], tasks=[research_task, writing_task])


result = workflow.kickoff()


print( result )
