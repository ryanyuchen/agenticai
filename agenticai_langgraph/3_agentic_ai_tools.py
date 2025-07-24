# define tools
## define arxiv and wikipedia
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper

api_wrapper_arxiv = ArxivAPIWraper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_warpper_arxiv, description="Query arxiv pappers")
arxiv.invoke("What is the latest research on quntuum computing")

api_wrapper_wiki = WikipediaAPIWraper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_warpper_wiki, description="Query wikipedia content")
wiki.invoke("Attention is all your need")

## definde tavily search tool for internet search
from langchain_community.tools.tavily_search import TavilySearchResutls

tavily = TavilySearchResults()
tavily.invoke("Provide me the recent AI news")

## combine all these tools in the list
tools = [arxiv, wiki, travily]

# Initialize the LLM model
from langchain_groq import ChatGroq

llm = ChatGroq(model="qwen-qwq-32b")
llm.invoke("What is the best team in England Premier League")

## combine llm with tools
llm_with_tools = llm.bind_tools(tools=tools)
llm_with_tools.invoke("What is the recent news on AI")

# Workflow
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage   ## Human message or AI message
from typing import Annotated   ## labelling
from langgraph.graph.message import add_messages  ## reducers in Langgraph

## define state schema
class State(TypedDict):
    message: Annotated[list[AnyMessage], add_messages]  ## keeping appending messages to Annotated

## build graph
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

def tool_calling_llm(state: State):
    return {"message": llm_with_tools.invoke(state["message"])}

builder = StateGraph(State)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()

# execution
messages = graph.invoke({"messages": "1706.03762"})
for m in messages["messages"]:
    m.pretty_print()

messages = graph.invoke({"messages": "Hi, my name is Tom"})
for m in messages["messages"]:
    m.pretty_print()

