📘 Project Description
AI Story Generator is a LangGraph-based application that creates short, age-appropriate bedtime stories for children aged 5–10 guided by previously collected user feedback to continuously improve storytelling quality.

▶️ Execution Flow:
- Story Generation: The story_generator node generates the story using the retriever tool. This tool provides user feedback from previously generated stories.

- Story Judging: After generating the story, it is passed to the LLMJudge. This is where I used human-in-the-loop that interprets the graph to get user feedback (to provide this feedback, I used Agent Inbox [https://github.com/langchain-ai/agent-inbox], a user interface for feedback collection. As of now, I have not created a custom user interface; I am using this existing one).

- Feedback Writing: After receiving the user feedback, it is passed to the write_feedback node to summarize and write the feedback to the vector database. This vector database will be used by the story_generator node through the retriever tool to guide future story generations.

▶️ Execution Steps:
- Install dependencies:
   pip install -r requirements.txt

- Run the graph using LangGraph CLI
   langgraph dev

- Set up Agent Inbox for human-in-the-loop feedback
   git clone https://github.com/langchain-ai/agent-inbox.git
   cd agent-inbox
   yarn install
   yarn dev

- Graph Execution using Langsmith: https://smith.langchain.com/public/460f3248-95ad-4093-8e82-db2f3c70b69e/r
- To view the block diagram, please refer to mermaid_diagram.png or Block Diagram.png.![alt text](<Block Diagram.png>)
- LangSmith execution before interpreter ![alt text](<Graph before interpreter.png>)
- LangSmith execition after interpreter ![alt text](<Graph after Interpreter.png>)
