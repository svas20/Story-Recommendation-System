from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def db_generator():
    response = "The user is interested in fairy tales, moral stories, and animal stories."
    document = Document(
    page_content=response,
    metadata={"source": "Feedback"},
    )
    vectorstore = FAISS.from_documents([document], embedding=OpenAIEmbeddings())
    vectorstore.save_local("feedback")