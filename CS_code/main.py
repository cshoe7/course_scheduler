"""
uvicorn main:app --reload --port 8000
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

#web framework that handles HTTP requests
app = FastAPI()

#lets browser front end talk to this script
app.add_middleware(
    CORSMiddleware,
    #any font end domain
    allow_origins=["*"],
    #POST requests only
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

#ollama API
client = Client(
    host = "https://ollama.com",
    headers = {'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

#loads embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#stores embedded chunks
vectorstore = FAISS.from_documents(chunks, embeddings)

#system prompt
prompt = """ 
    You are an expert in the Ursinus College course catalog. Students will ask you questions about the courses offered at Ursinus college, 
    and you will answer correctly and conciselly. Only recommend courses that explicitly appear in the retrieved context. 
    If a course is not in the context provided, do not mention it. If something is unclear, you will follow up with a clarifying question. Assume all prerequisits are
    satisfied. DO NOT make the output one block of text. Make sure paragraphs are broken up accordingly, and spacing is correct. The following are types of 
    questions you may recieve and how you will answer them:

    #####Question 1#####
    If the user asks for a schedule, this is the structure you should respond in:

    Fall
    Course1ID: CourseName - Brief Description
    Course2ID: CourseName - Brief Description
    Course3ID: CourseName - Brief Description
    Course4ID: CourseName - Brief Description

    Spring
    Course5ID: CourseName - Brief Description
    Course6ID: CourseName - Brief Description
    Course7ID: CourseName - Brief Description
    Course8ID: CourseName - Brief Description

    #####Question 2#####
    If the user asks you to make changed to the outputed schedule, make the appropriate changes and output the new schedule

    #####Question 3#####
    If you user asks for courses that fulfill a certain requirement, follow up and ask them what topics they are intested in to narrow the search

    #####Question 4#####
    If the user asks for course reccomendations based on a certain interest, reccomend a course that is relevant to that interest

 """

print("Ready.")


#defines shape of expected POST request - JSON w/ message fiel
class Message(BaseModel):
    message: str

#registers route at /recommend
#parses request into message object
@app.post("/recommend")
async def recommend(payload: Message):

    #user input
    query = payload.message
    #runs a similarity search on the query and finds the top 6 most similar chunks to the query
    retrieved = vectorstore.similarity_search(query, k=6)
    #joins the chunks together to form the context
    context = "\n\n".join([doc.page_content for doc in retrieved])

    #determinds the LLM behavior
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

    #generator function, yeilds each chunk as it gets it from the llm
    def stream_response():
        for part in client.chat("gpt-oss:120b", messages=messages, stream=True):
            yield part["message"]["content"]

    #StreamingResponse gives the typing effect
    return StreamingResponse(stream_response(), media_type="text/plain")




