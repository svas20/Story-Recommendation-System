from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
class State(TypedDict):
    messages: Annotated[list, add_messages]
    feedback_log: str  

class ConfigSchema(TypedDict):
    model: str
    thread_id:str
