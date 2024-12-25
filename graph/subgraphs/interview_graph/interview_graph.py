
from langgraph.pregel import RetryPolicy
from graph.state import InterviewState
from langgraph.graph import START,END, StateGraph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from graph.subgraphs.interview_graph.nodes.generate_answer import generate_answer
from graph.subgraphs.interview_graph.nodes.generate_question import generate_question
from graph.subgraphs.interview_graph.nodes.generate_answer import generate_answer
from graph.subgraphs.interview_graph.consts import ANSWER_QUESTION_NODE,ASK_QUESTION_NODE
import asyncio


max_num_turns = 5
def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return END
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return END
    return ASK_QUESTION_NODE


builder = StateGraph(InterviewState)

builder.add_node(ASK_QUESTION_NODE, generate_question, retry=RetryPolicy(max_attempts=5))
builder.add_node(ANSWER_QUESTION_NODE, generate_answer, retry=RetryPolicy(max_attempts=5))

builder.add_edge(START, ASK_QUESTION_NODE)
builder.add_edge(ASK_QUESTION_NODE, ANSWER_QUESTION_NODE)
builder.add_conditional_edges(ANSWER_QUESTION_NODE, route_messages)

interview_graph = builder.compile(checkpointer=False).with_config(
    run_name="Conduct Interviews"
)
