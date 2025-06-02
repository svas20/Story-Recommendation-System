from config import State, ConfigSchema
from langgraph.graph import END, StateGraph, START
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from LLMJudge import LLMJudge
from write_feedback import write_feedback
from story_generator import story_generator
from retriver import get_retriever_tool
from langgraph.prebuilt import ToolNode
from db_generate import db_generator
from datetime import datetime
import os
load_dotenv()

if not os.path.exists("feedback"): 
    db_generator()                          #creates a database that can be used to store user feedback.
retriever_tool = get_retriever_tool()

def condition(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "LLMJudge"
    else:
        return "retrieve"

builder = StateGraph(State, config_schema=ConfigSchema)
today_date = datetime.today().strftime("%m/%d/%Y")
config = {"configurable": {"model":  os.getenv("MODEL"), "thread_id":f"story_{today_date}"}}
builder.add_node("story_generator", story_generator)        #Generates the story
builder.add_node("retrieve",ToolNode([retriever_tool]))     #Retrieve the feedback  
builder.add_node("LLMJudge",LLMJudge)                       #Get the user feedback
builder.add_node("write_feedback", write_feedback)          #writes the feedback to DB

builder.add_edge(START, "story_generator")
builder.add_conditional_edges("story_generator",condition, {"retrieve":"retrieve","LLMJudge":"LLMJudge"})
builder.add_edge("retrieve", "story_generator")
builder.add_edge("LLMJudge","write_feedback")
builder.add_edge("write_feedback",END)

checkpointer = InMemorySaver()
graph = builder.compile()                                  
#graph = builder.compile(checkpointer=checkpointer)        # Uncomment the following line if you want to execute the workflow without using LangGraph Studio and comment the above line

graph_dia = graph.get_graph().draw_mermaid_png()
with open("mermaid_diagram.png", "wb") as f:        
    f.write(graph_dia)

if __name__ == "__main__":
    def graph_input(input):
        for message_chunk, metadata in graph.stream(input, config=config, stream_mode="messages"):
            if message_chunk.content:
                print(message_chunk.content, end="", flush=True)
       
    user_input = input("What bedtime story would you like to hear?: ")
    story_request = {"messages":[HumanMessage(content=user_input)]}
    graph_input(story_request)
     

        
 







