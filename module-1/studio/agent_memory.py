from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os

load_dotenv()


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]


llm = ChatOpenAI(base_url=os.getenv("OPENAI_API_BASE"), api_key=os.getenv("OPENAI_API_KEY"))
llm_with_tools = llm.bind_tools(tools)


# System Instruction
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")


# creating Node

def assistant(state: MessagesState) -> MessagesState:
    return {"messages": llm_with_tools.invoke([sys_msg] + state["messages"])}

# building Graph
builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

memory = MemorySaver()

graph = builder.compile(memory)


config = {"configurable":{"thread_id":10}}

messages = [HumanMessage(content=f"add 5 and 6")]

messages = graph.invoke({"messages":messages}, config)

for m in messages["messages"]:
    print(m.pretty_print())


messages = [HumanMessage(content=f"multiply with 100")]

messages = graph.invoke({"messages":messages}, config)

for m in messages["messages"]:
    print(m.pretty_print())
