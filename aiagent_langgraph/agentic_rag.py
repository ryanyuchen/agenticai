from langgraph import StateGraph
from langgraph import workflow
from langchain_community import WebBaseLoader

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings("all-MiniLM-L6-V2")

urls = [
    "https://lilianwen.github.com/posts/2023-06-23-agent"
]
docs = [WebBaseLoader(url).load() for url in urls]

docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharactorTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=100)

doc_splits = text_splitter.split_documents(docs_list)

vectordb = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chrome",
    embedding=embeddings
)

retriever = vectordb.as_retriver()

retriver_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
)

tools = [retirever_tool]

def AI_Assistant(state: AgentState):
    print("---call agent---")
    messages = state["messages"]
    llm_with_tool = llm.bind_tools(tools)
    response = llm_with_tool.invoke(messages)
    return {"messages": [response]}

# def retireve(state):
#     pass

def rewrite(state: AgentState):
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f"""
            Look at th einput and try to reason about the underlying material
            \n ----- \n
            {question}
            \n ----- \n
            Formulate an improved question:
            """
        )
    ]

    response = llm.invoke(msg)
    return {"messages": [response]}

def generate(state: AgentState):
    messages=state["messages"]
    question = messages[0].content
    last_message = message[-1]
    docs = last_message.content

    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = promt | llm | StrOutputParser()

    response = rag_chain.invoke({"context": docs, "question": question})

    return {"messages": [response]}

def grade_documents(state) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM
    model = ChatOpenAI(temperature=0, model="gpt-4-0125-preview", streaming=True)

    # LLM with tool and validation
    llm_with_tool = model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # Chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "rewrite"

class grade(BaseModel):
    binary_score:str = Field()

class AgentState(TypeDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]



workflow=StateGraph(AgentState)
workflow.add_node("ai_assistant", AI_Assistant)
retrieve = ToolNode([retriever_tool])
workflow.add_node("retriever", retrieve)
workflow.add_node("rewriter", rewrite)
workflow.add_node("generator", generate)

workflow.add_edge(START, "ai_assistant")
workflow.add_conditional_edges("ai_assistant", tools_condition, {"tools": "retriever", END: END})
workflow.add_conditional_edges("retriver", grade_dcouments, {"rewriter": "rewriter", "generator": "generator"})
workflow.add_edge("generator", END)
workflow.add_edge("rewriter": "ai_assistant")

app = workflow.compile()

app.invoke("")