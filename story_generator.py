from config import State
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from retriver import get_retriever_tool
from langgraph.prebuilt import ToolNode
load_dotenv()

def story_generator(state:State,config):
    GENERATOR_PROMPTS =""" Write a short bedtime story using simple vocabulary suitable for children aged 5 to 10.
                            - Use age-appropriate words throughout the story.
                            - Ensure the story is gentle, imaginative, and calming, with a simple moral at the end..
                            - Consider the latest dated feedback from the feedback tool to guide the story.
                            - The feedback contains summaries of previously generated stories—avoid repeating those storylines."""
     
    model = init_chat_model(model=str(config["configurable"]["model"]),temperature = 0.7)
    retriever_tool = get_retriever_tool()
    model_with_tools = model.bind_tools([retriever_tool])
    story_response = model_with_tools.invoke(
    [{"role":"system","content":GENERATOR_PROMPTS},
    *state["messages"]
    ])
    return {"messages": state["messages"] + [story_response]}


