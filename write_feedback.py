from config import State
from typing import Optional
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_core.documents import Document
load_dotenv()


def write_feedback(state:State,config):
    FEEDBACK_PROMPTS ="""You are a feedback summarizer for a bedtime storytelling assistant. Your task is to review the feedback_log and generate a brief summary in 2–3 sentences that can help guide future story generations.
                            Instructions:
                            - If feedback was provided, include the feedback line and summarize the story along with what the user liked or disliked.
                            - If no feedback was given, summarize the query and type of story the user requested and the story that was generated.
                            - Include the date in the summary.
                        """
    
   
    model = init_chat_model(model=str(config["configurable"]["model"]),temperature = 0.1)
    Judge_response = model.invoke([
        {"role": "system", "content": FEEDBACK_PROMPTS},
         *state["messages"],
         state["feedback_log"]
    ])
    print(Judge_response)
    document = Document(
    page_content=Judge_response.content,
    metadata={"source": "Feedback"},
    )
    vectorstore = FAISS.load_local("feedback", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    vectorstore.add_documents([document])
    vectorstore.save_local("feedback")
