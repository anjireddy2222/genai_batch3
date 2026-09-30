from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import openai
from pypdf import PdfReader
from docx import Document

app = FastAPI()


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
    chunk_size = 50
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
    

    return { "message": "ok", "data": data, "chunks": chunks }




