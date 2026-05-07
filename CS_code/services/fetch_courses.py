"""
gets a list of courses that fulfill a certain requirement
"""

import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from ollama import Client


#parses the pdf
loader = PyMuPDFLoader("/Users/claireshoemaker/course_scheduler/CS_code/data/UCcc2025.pdf")
#loads the context
docs = loader.load() 

#sliding window of context
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, #how many characters it looks at at once
    chunk_overlap = 200 #charcaters that overlap in each chunk
)

#splits up the document into chunks
chunks = splitter.split_documents(docs)

client = Client(
    host = "https://ollama.com",
    headers = {'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)

query = "What courses do I have to take for a computer science major?"
retrieved = vectorstore.similarity_search(query, k=3)
context = "\n\n".join([doc.page_content for doc in retrieved])

messages = [
    {
        "role": "user",
        "content": f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}"
    }
]

for part in client.chat("gpt-oss:120b", messages=messages, stream=True):
    print(part["message"]["content"], end="", flush=True)

"""
TODO: 
- figure out where all of this rag setup code should go
- add steps to the final report/setup instructions
- do some prompt engineering to get better outputs
- hook all of this up to the UI
"""