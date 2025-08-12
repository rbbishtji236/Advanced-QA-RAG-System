
from typing import Optional
import os

# no key needed for DuckDuckGo
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults

try:
    from langchain_community.tools import TavilySearchResults
    _HAS_TAVILY = True
except Exception:
    _HAS_TAVILY = False


def load_tavily_search_tool(tavily_search_max_results: int, provider: Optional[str] = None):
    """
    Load a web search tool.

    Defaults to DuckDuckGo (free, no key).
    If provider='tavily' and Tavily is installed + key configured, uses Tavily.

    Args:
        tavily_search_max_results: max results to return
        provider: 'ddg' | 'tavily' | 'auto' (None/'auto' -> ddg)
    """
    provider = (provider or os.getenv("SEARCH_PROVIDER", "ddg")).lower()

    if provider == "tavily":
        if not _HAS_TAVILY:
            raise ImportError("Tavily tool not installed. Use provider='ddg' or install tavily tool.")
        return TavilySearchResults(max_results=tavily_search_max_results)

    return DuckDuckGoSearchResults(max_results=tavily_search_max_results)
