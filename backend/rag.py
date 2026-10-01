from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import openai
from pypdf import PdfReader
from docx import Document
import chromadb
import uuid
from pydantic import BaseModel


app = FastAPI()

openai_client = openai.OpenAI( api_key= "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")
chromdb_client = chromadb.PersistentClient("./vector_db")
courses_collection = chromdb_client.get_or_create_collection(name="courses3")
terms_collection = chromdb_client.get_or_create_collection(name="terms_privacy_data")

def process_pdf(file):
    print("processing pdf file")
    pdf_reader = PdfReader(file.file)
    data = ""
    for page in pdf_reader.pages:
        data = data + page.extract_text()

    return data



def process_doc(file):
    print("processing doc file")
    doc_reader = Document(file.file)
    data = ""
    for para in doc_reader.paragraphs:
        data = data + para.text
    
    return data


def process_txt(file):
    print("processing text file")
    data = file.file.read()
    return data

# 
# 3 chars
"""
abc
def
ghi
jkl
mno
pqr
stu
vwx
yz


a b c d e f
0 1 2 3 4 5

1000 chars
length = 2 chars
500 chunks

0 -> 2 chars: 

"""
def convert_to_chunks(data):
    print("converting to chunks")
    no_of_chars = len(data)
    chunk_size = 250
    chunks = []
    for index in range( 0, no_of_chars, chunk_size ):
        chunks.append( data[index : index + chunk_size ])

    return chunks




@app.post("/add-files")
def add_files( file : UploadFile = File(...) ):

    file_name = file.filename
    data = ""

    if file_name.endswith(".pdf") ==  True:
        data = process_pdf(file)

    if file_name.endswith(".txt") == True:
        data = process_txt(file)

    if file_name.endswith(".docx") == True or file_name.endswith(".doc") == True:
        data = process_doc(file)

    chunks = convert_to_chunks(data)
    vector_data = ""
    responses = []
    for chunk in chunks:
        vectors = openai_client.embeddings.create(input=chunk, model="text-embedding-3-small")
        vector_data = vectors.data[0].embedding
        chunk_id = uuid.uuid4()
        courses_collection.add( ids=[str(chunk_id)], embeddings=[vector_data], documents=[chunk]  )
        responses.append( { 'id': str(chunk_id), 'embeddings':vector_data, 'documents': chunk  } )

        

    

    return { "message": "ok", "data": data, "chunks": responses }


class RagChatInputData(BaseModel):
    user_msg: str


@app.post("/chat")
def rag_chat( req : RagChatInputData ):

    vectors = openai_client.embeddings.create(input=req.user_msg, model='text-embedding-3-small')
    vector_data = vectors.data[0].embedding

    embed_results = courses_collection.query( query_embeddings=[vector_data], n_results = 3 )
    business_knowledge = ""
    for embed in embed_results:
        business_knowledge = business_knowledge + " " + embed

    prompt = f""" 
        you are AI sales assistant for softwareschool. we are providing coding classes in telugu. 
    
        You help students to choose right course based on thei background and expereince, answer their questions, and guide them to choose right course.
    
        Rules & Instructions
    
        1. keep responses short 3 to 6 lines only
        2. use friendly and professional language
        3. use simple english and always reply in english only
        4. ask 1 or 2 questions ata a time
        5. if you don't know the answer, please escalate o human support
        6. if user is agressive, connect to human
        7. never promise job guarantee
        8. dont imagine and give answers, if the data is not availbale in our business knowledge, connect with our team.

        Business data:
        {business_knowledge}
    
        User message: { req.user_msg }
    """

    ai_response = openai_client.responses.create(input=prompt, model="gpt-5.5")




    return { "response": ai_response }
 


