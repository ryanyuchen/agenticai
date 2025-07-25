from langgraph.graph import Graph, Node, Edge
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama3-70b-instruct")

def function1(input):
    return llm.invoke(input).content

def function2(input):
    upper_string = input.upper()
    return upper_string

workflow = Graph()
workflow.add_node("function1", function1)
workflow.add_node("function2", function2)

workflow.add_edge("function1", "function2")
workflow.set_entry_point("function1")
workflow.set_finish_point("function2")

app = workflow.compile()

app.invoke()
