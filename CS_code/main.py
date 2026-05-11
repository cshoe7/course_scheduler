"""
gets a list of courses that fulfill a certain requirement
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from ollama import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

print("Loading and indexing PDF...")
#parses the pdf
loader = PyMuPDFLoader("/Users/claireshoemaker/course_scheduler/CS_code/data/UCcc2025.pdf")
#loads the context
docs = loader.load() 

#sliding window of context
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000, #how many characters it looks at at once
    chunk_overlap = 400 #charcaters that overlap in each chunk
)

#splits up the document into chunks
chunks = splitter.split_documents(docs)

client = Client(
    host = "https://ollama.com",
    headers = {'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)

prompt = """ 
    You are an expert in the Ursinus College course catalog. Students will ask you questions about the courses offered at Ursinus college, 
    and you will answer correctly and conciselly. You will not hallucinate any answers. You will cite the page of the course catalog you 
    get your information from. If something is unclear, you will follow up with a clarifying question. If the The following are types of questions 
    you may recieve and how you will answer them:

    If the user asks for a list of courses that fulfill a reuirement, you will explain what the requiremnent is, then you will list the courses that
    fulfill it. You should include a summary of the course description. List 10-15 courses as examples, then ask what the users interests are to help 
    narrow down the options.


 """

print("Ready.")



# --- Request schema ---
class Message(BaseModel):
    message: str

# --- Streaming endpoint ---
@app.post("/recommend")
async def recommend(payload: Message):

    query = payload.message
    retrieved = vectorstore.similarity_search(query, k=6)
    context = "\n\n".join([doc.page_content for doc in retrieved])

    print(context)


    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}"
        }
    ]

    def stream_response():
        for part in client.chat("gpt-oss:120b", messages=messages, stream=True):
            yield part["message"]["content"]

    return StreamingResponse(stream_response(), media_type="text/plain")



"""
TODO: 
- figure out where all of this rag setup code should go
- add steps to the final report/setup instructions
- do some prompt engineering to get better outputs
- hook all of this up to the UI
"""