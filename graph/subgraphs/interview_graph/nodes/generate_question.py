
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import MessagesPlaceholder
from graph.state import InterviewState
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import chain as as_runnable
from graph.subgraphs.interview_graph.chains.generate_question_chain import build_gn_chain

@as_runnable
async def generate_question(state: InterviewState):
    editor = state["editor"]
    gn_chain= build_gn_chain(editor)
    result = await gn_chain.ainvoke(state)
    return {"messages": [result]}


