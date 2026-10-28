"""
pip install mcp
"""
from mcp.server.mcpserver import MCPServer

mcp_server = MCPServer()


@mcp_server.tool( name="get_courses_list",  description="use this tool to get all available courses" )
def get_courses_list():
    courses_list = [
        { "name": "ReactJS", "type": "Recorded" },
        { "name": "GenAI", "type": "Live" },
        { "name": "Springboot", "type": "Recorded" }
    ]
    return courses_list


@mcp_server.tool( name="get_syllabus_demo_links",  description= "use this tool to get course syllabus and demo links")
def get_syllabus_demo_links():
    syllabus_demo_list = [
        { "name": "ReactJS", "syllabus": "http://reactjs-syllabus.com", "demo": "http://reactjs-demo.com" },
        { "name": "genai", "syllabus": "http://genai-syllabus.com", "demo": "http://genai-demo.com" },
        { "name": "Springboot", "syllabus": "http://spring-syllabus.com", "demo": "http://spring-demo.com" }
    ]
    return syllabus_demo_list


app = mcp_server.streamable_http_app()

# http://127.0.0.1:8000/mcp

