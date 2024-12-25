
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import START,END, StateGraph
from graph.consts import INIT_RESEARCH, CONDUCT_INTERVIEW_NODE, REFINE_OUTLINE_NODE, INDEX_REFERENCES_NODE, \
    WRITE_SECTIONS_NODE, WRITE_ARTICLE_NODE
from graph.state import ResearchState

from graph.nodes import init_research_node, conduct_interviews, refine_outline, index_references, write_sections, write_article
from graph.subgraphs.interview_graph import interview_graph

from langgraph.pregel import RetryPolicy
from graph.state import InterviewState
from langchain_core.messages import AIMessage

workflow = StateGraph(ResearchState)

workflow.set_entry_point(INIT_RESEARCH)
workflow.add_node(INIT_RESEARCH, init_research_node)
workflow.add_node(CONDUCT_INTERVIEW_NODE, conduct_interviews)
workflow.add_node(REFINE_OUTLINE_NODE, refine_outline)
workflow.add_node(INDEX_REFERENCES_NODE, index_references)
workflow.add_node(WRITE_SECTIONS_NODE, write_sections)
workflow.add_node(WRITE_ARTICLE_NODE, write_article)

workflow.add_edge(INIT_RESEARCH,CONDUCT_INTERVIEW_NODE)
workflow.add_edge(CONDUCT_INTERVIEW_NODE,REFINE_OUTLINE_NODE)
workflow.add_edge(REFINE_OUTLINE_NODE,INDEX_REFERENCES_NODE)
workflow.add_edge(INDEX_REFERENCES_NODE,WRITE_SECTIONS_NODE)
workflow.add_edge(WRITE_SECTIONS_NODE,WRITE_ARTICLE_NODE)
workflow.add_edge(WRITE_ARTICLE_NODE,END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
