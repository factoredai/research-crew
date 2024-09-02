from typing import Dict, List

from reportgen_agent.core.state import ReportGenState


def generate_citations(search_results: List[Dict[str, str]]) -> str:
    """
    Placeholder function to generate citations for the sources used.

    Args:
        search_results (List[Dict[str, str]]): A list of search results where each result is a dictionary
                                               containing at least 'title' and 'url' keys.

    Returns:
        str: A Markdown formatted string containing the citations.
    """
    # Placeholder implementation: Simple list of sources
    citations = "## References\n"
    for idx, result in enumerate(search_results, start=1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        citations += f"{idx}. [{title}]({url})\n"
    return citations


def add_citations(state: ReportGenState) -> Dict:
    """
    Add citations to the generated Markdown report and update the state.

    Args:
        state (ReportGenState): The current state of the workflow.

    Returns:
        Dict: The updated state with the Markdown report containing citations.
    """

    # Generate citations based on the search results
    citations = generate_citations(state["search_results"])

    # Append the citations to the existing Markdown report
    state["markdown_report"] += "\n" + citations

    # Return the updated state
    return state
