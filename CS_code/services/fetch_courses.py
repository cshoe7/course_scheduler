"""
gets a list of courses that fulfill a certain requirement
"""

import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from ollama import Client


#wrapper
class OllamaEmbeddings(Embeddings):
    def __init__(self, client, model):
        self.client = client
        self.model = model
    
    def embed_documents(self, texts):
        return [self.client.embeddings(model = self.model, input = t).embeddings[0] for t in texts]
    
    def embed_query(self, text):
        return self.client.embeddings(model = self.model, input=text).embeddings[0]


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

embeddings = OllamaEmbeddings(client, model = "nombic-embed-text")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.similarity_search(chunks, embeddings)

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
- set environment variable
- figure out where all of this rag setup code should go
"""