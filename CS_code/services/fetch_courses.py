"""
gets a list of courses that fulfill a certain requirement
"""

import os
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

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

#embedder
embeddings = OllamaEmbeddings(
    model="qwen3-embedding",  
    base_url="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}
)

"""
TODO: 
- set environment variable
- set up vector store and retriever, then try to test everything
- figure out where all of this rag setup code should go
"""