from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from openai import AsyncOpenAI
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

load_dotenv()


app = FastAPI()
openai_voice_client = AsyncOpenAI()

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


ai_agent = create_agent("openai:gpt-5.5", tools=[ss_tool], system_prompt="you are ai sales agent for softwareschool, we are providng coding classes in telugu, undertsnad user background, goals and suggest best courses")


@app.post("/voice-chat")
async def voice_chat( file : UploadFile = File(...) ):

    AUDIO_FILE_FORMATS = [ ".mp3", ".mp4", ".mpeg", ".wav", ".webm", ".flac", ".m4a" ]
    filename = file.filename
    ext = Path(filename).suffix.lower()

    if ext not in AUDIO_FILE_FORMATS:
        return { "result": "failed", "message": "only audio files supported" }

    audio_bytes = await file.read()

    if not audio_bytes:
        return { "result": "failed", "message": "audio file is empty" }

    transcription = await openai_voice_client.audio.transcriptions.create(
        model="gpt-transcribe",
        file=(
            filename, audio_bytes, file.content_type
        )
    )

    transcription = transcription.text

    ai_response = ai_agent.invoke({
        "messages": [
            { "role": "user", "content": transcription }
        ]
    })





    return { "data": ai_response }


