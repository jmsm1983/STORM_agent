from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

tavily_search = TavilySearchResults(max_results=4)

@tool
def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]