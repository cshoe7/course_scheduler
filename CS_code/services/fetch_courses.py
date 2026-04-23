"""
gets a list of courses that fulfill a certain requirement
"""

import os
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

#where the rag info lives in vectorized form
vectorstore = Chroma.from_documents(chunks, embeddings)
#retrives the info from the vector store
retriever = vectorstore.as_retriever()


llm = ChatOllama(
    model = "gpt-oss:120b",
    base_url = "https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}
)

prompt = ChatPromptTemplate.from_template("""

Answer the question based only on the following context: {context}

Question: {question}

""")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke("What types of courses do I have to take as a computer science major?"))

"""
TODO: 
- set environment variable
- figure out where all of this rag setup code should go
"""