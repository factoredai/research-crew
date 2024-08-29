import os
from abc import ABC, abstractmethod
from ast import literal_eval
from typing import Dict, List, Type

from langchain_community.tools import (
    BingSearchResults,
    BraveSearch,
    TavilySearchResults,
)
from langchain_community.utilities import SerpAPIWrapper
from langchain_google_community import GoogleSearchResults

from reportgen_agent.config import settings
from reportgen_agent.core.state import ReportGenState


class SearchProvider(ABC):
    """Abstract base class for search providers."""

    @abstractmethod
    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform a web search using the provider's API.

        Parameters
        ----------
        query : str
            The search query string.
        num_results : int
            The number of search results to return.

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries, where each dictionary represents a
            search result with 'title', 'snippet', and 'link' keys.
        """
        pass


class SerpAPISearchProvider(SearchProvider):
    """Search provider implementation for SerpAPI."""

    def __init__(self):
        self.search_engine = SerpAPIWrapper(serpapi_api_key=settings.web_search.serpapi_api_key)

    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        # TODO: Doesn't support number of search results??
        # params = {"num": num_results}
        params = {}
        results = self.search_engine.results(query, **params)
        return [
            {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", ""),
            }
            for result in results.get("organic_results", [])
        ]


class GoogleSearchProvider(SearchProvider):
    """Search provider implementation for Google Custom Search API."""

    def __init__(self):
        self.search_tool = GoogleSearchResults(
            google_api_key=settings.web_search.google_api_key,
            google_cse_id=settings.web_search.google_cse_id,
        )

    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        results = self.search_tool.results(query=query, num_results=num_results)
        return [
            {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", ""),
            }
            for result in results
        ]


class BingSearchProvider(SearchProvider):
    """Search provider implementation for Bing Search API."""

    def __init__(self):
        self.search_tool = BingSearchResults(
            bing_subscription_key=settings.web_search.bing_subscription_key,
            bing_search_url=settings.web_search.bing_search_url,
        )

    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        results = self.search_tool.run(f"{query}, num_results={num_results}")
        return [
            {
                "title": result.get("name", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("url", ""),
            }
            for result in results
        ]


class BraveSearchProvider(SearchProvider):
    """
    Search provider implementation for Brave Search API.
    """

    def __init__(self):
        self.search_tool = BraveSearch.from_api_key(
            api_key=settings.web_search.brave_api_key,
            search_kwargs={"count": settings.web_search.num_results},
        )

    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        results = self.search_tool.run(query)
        print(results)
        return [
            {
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", ""),
            }
            for result in literal_eval(results[:num_results])
        ]


class TavilySearchProvider(SearchProvider):
    """
    Search provider implementation for Tavily Search API.
    """

    def __init__(self):
        self.original_api_key = os.environ.get("TAVILY_API_KEY")
        os.environ["TAVILY_API_KEY"] = settings.web_search.tavily_api_key

        self.search_tool = TavilySearchResults(
            max_results=settings.web_search.num_results,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True,
        )

    def search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        results = self.search_tool.invoke({"query": query})
        return [
            {
                "title": result.get("title", ""),
                "snippet": result.get("content", ""),
                "link": result.get("url", ""),
            }
            for result in results[:num_results]
        ]

    def __del__(self):
        """Restore the original API key when the object is destroyed."""
        if self.original_api_key is not None:
            os.environ["TAVILY_API_KEY"] = self.original_api_key
        else:
            os.environ.pop("TAVILY_API_KEY", None)


def get_search_provider() -> SearchProvider:
    """
    Factory function to get the appropriate search provider based on configuration.

    Returns
    -------
    SearchProvider
        An instance of the configured search provider.

    Raises
    ------
    ValueError
        If an unsupported search provider is specified in the configuration.
    """
    provider_name = settings.web_search.provider.lower()
    providers: Dict[str, Type[SearchProvider]] = {
        "serpapi": SerpAPISearchProvider,
        "google": GoogleSearchProvider,
        "bing": BingSearchProvider,
        "brave": BraveSearchProvider,
        "tavily": TavilySearchProvider,
    }
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unsupported search provider: {provider_name}")
    return provider_class()


def perform_web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search based on the query using the configured search
    provider.

    Parameters
    ----------
    query : str
        The search query.
    num_results : int, optional
        The number of search results to return, by default 5.

    Returns
    -------
    List[Dict[str, str]]
        A list of search results, where each result is a dictionary
        with keys 'title', 'snippet', and 'link'.
    """
    try:
        search_provider = get_search_provider()
        return search_provider.search(query, num_results)
    except Exception as e:
        print(f"Error performing web search: {str(e)}")
        return []


def perform_web_search_node(state: ReportGenState, run_dir: str) -> Dict:
    """
    Perform a web search using the keywords or expanded concepts and
    update the state.

    Parameters
    ----------
    state : ReportGenState
        The current state of the workflow.
    run_dir : str
        The directory where run-specific data is stored.

    Returns
    -------
    Dict
        The updated state with the search results added.
    """
    keywords = state.get("keywords", [])
    expanded_concepts = state.get("expanded_concepts", [])
    search_terms = keywords + expanded_concepts
    search_query = state.get("query", "") + " " + " ".join(search_terms[: settings.web_search.max_search_terms])

    print(f"{search_query = }")
    search_results = perform_web_search(query=search_query, num_results=settings.web_search.num_results)

    documents = [
        {
            "title": result.get("title", ""),
            "snippet": result.get("snippet", ""),
            "url": result.get("link", ""),
        }
        for result in search_results
    ]

    state["search_results"] = documents
    state["search_query"] = search_query

    # Return the updated state
    return state
