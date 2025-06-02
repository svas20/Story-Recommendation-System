from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

def get_retriever_tool():
    vectorstore = FAISS.load_local(
        "feedback",
        embeddings=OpenAIEmbeddings(),
        allow_dangerous_deserialization = True  
    )
    retriever = vectorstore.as_retriever()
    return create_retriever_tool(
        retriever,
        name="feedback",
        description="Use feedback from previous stories to guide improvements."  
    )   