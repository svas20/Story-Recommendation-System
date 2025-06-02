from config import State
from dotenv import load_dotenv
from langgraph.types import interrupt, Command
from langgraph.prebuilt.interrupt import HumanInterrupt
import os
from datetime import datetime

load_dotenv()

def LLMJudge(state:State):
    request: HumanInterrupt = {
        "action_request":{
                "action": "Feedback",
                "args":{ state["messages"][-1].content,
                        state["messages"][0].content
                }
        },
        "config": {
            "allow_ignore": True,
            "allow_respond": True,
            "allow_edit": False,
            "allow_accept": False
        },
        "description": "Please provide the Feedback"
    }
     
    response = interrupt([request])
    today_date = datetime.today().strftime("%m/%d/%Y")
    if response[0]["type"] == "response":
       return Command(goto=["write_feedback"],update={"feedback_log":f"Feedback: {today_date} {response[0]['args']}"})
    if response[0]["type"] == "ignore":
        return Command(goto=["write_feedback"], update={"feedback_log": f"Feedback ({today_date}): ⟨not provided⟩"})