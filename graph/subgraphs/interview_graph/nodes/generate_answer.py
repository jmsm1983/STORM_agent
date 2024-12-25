import json

from typing_extensions import Optional
from langchain_core.runnables import RunnableConfig
from graph.state import InterviewState
from graph.subgraphs.interview_graph.chains.utils import swap_roles,tag_with_name
from graph.subgraphs.interview_graph.chains.generate_answer_chain import gen_answer_chain
from graph.subgraphs.interview_graph.chains.generate_queries_chain import gen_queries_chain
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from graph.subgraphs.interview_graph.tools.websearch import search_engine


async def generate_answer(
    state: InterviewState,
    config: Optional[RunnableConfig] = None,
    name: str = "Subject_Matter_Expert",
    max_str_len: int = 15000,
):
    swapped_state = swap_roles(state, name)  # Convert all other AI messages
    queries = await gen_queries_chain.ainvoke(swapped_state)

    query_results = await search_engine.abatch(
        queries["parsed"].queries, config, return_exceptions=True
    )

    successful_results = [
        res for res in query_results if not isinstance(res, Exception)
    ]

    all_query_results = {
        res["url"]: res["content"] for results in successful_results for res in results
    }

    # We could be more precise about handling max token length if we wanted to here
    dumped = json.dumps(all_query_results)[:max_str_len]
    ai_message: AIMessage = queries["raw"]
    tool_call = queries["raw"].tool_calls[0]
    tool_id = tool_call["id"]
    tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)
    swapped_state["messages"].extend([ai_message, tool_message])
    # Only update the shared state with the final answer to avoid
    # polluting the dialogue history with intermediate messages
    generated = await gen_answer_chain.ainvoke(swapped_state)

    cited_urls = set(generated["parsed"].cited_urls)

    # Save the retrieved information to a the shared state for future reference
    cited_references = {k: v for k, v in all_query_results.items() if k in cited_urls}

    formatted_message = AIMessage(name=name, content=generated["parsed"].as_str)

    return {"messages": [formatted_message], "references": cited_references}