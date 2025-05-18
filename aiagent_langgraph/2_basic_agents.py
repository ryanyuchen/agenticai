# define state schema, which serves as the input schema for all nodes and edges in the graph
from typing_extensions import TypeDict

class State(TypeDict):
    graph_info: str

# define nodes
def start_play(state: State):
    print("Start Play node has been called")
    return {"graph_info": state["graph_info"] + "I am planning to play"}

def cricket(state: State):
    print("Cricket node has been called")
    return {"graph_info": state["graph_info"] + " Cricket"}

def badminton(state: State):
    print("Badminton node has been called")
    return {"graph_info": state["graph_info"] + " Badminton"}

# define conditional edge
import random
from typing import Literal

def random_play(state: State)-> Literal['cricket', 'badminton']:
    if random.random() > 0.5:
        return "cricket"
    else:
        return "badminton"

# construct entire graph
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)

## add ndoes
graph.add_node("start_play", start_play)
graph.add_node("cricket", cricket)
graph.add_node("badminton", badminton)

## add edges
graph.add_edge(START, "start_play")
graph.add_conditional_edge("start_play", random_play)
graph.add_edge("cricket", END)
graph.add_edge("badminton", END)

## compile the graph
graph_builder = graph.complie

# display graph
from IPython.display import Image, display
display(Image(graph_builder.get_graph().draw_mermaid_png()))

# execution
graph_builder.invoke({"graph_info": "My name is ABC."})
