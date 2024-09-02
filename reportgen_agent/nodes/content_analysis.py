from typing import List, Optional

from reportgen_agent.core.state import ReportGenState


def filter_and_rank_content(content_list: List[Optional[str]], keywords: Optional[List[str]] = None) -> List[str]:
    """Placeholder function to filter and rank content based on relevance to the keywords.

    Parameters
    ----------
    content_list : List[Optional[str]]
        A list of content strings to be filtered and ranked. May contain None values.
    keywords : Optional[List[str]], optional
        A list of keywords to determine relevance, by default None.

    Returns
    -------
    List[str]
        A list of filtered and ranked content.

    Notes
    -----
    This is a placeholder implementation that simply returns the content
    sorted by length as a dummy ranking. It filters out None values.
    """
    # Placeholder implementation: Just returns the content sorted by length as a dummy ranking
    return sorted(
        [content for content in content_list if content is not None],
        key=len,
        reverse=True,
    )


# TODO: This should be a whole subgraph in the future. "Garbage in,
# garbage out" also applies for report generation
def analyze_content(state: ReportGenState, run_dir: str) -> ReportGenState:
    """Analyze the filtered content and update the state with the summarized information.

    Parameters
    ----------
    state : ReportGenState
        The current state of the workflow.
    run_dir : str
        The directory where run-specific data is stored.

    Returns
    -------
    ReportGenState
        The updated state with the analyzed and summarized content.
    """

    analyzed_content = filter_and_rank_content(state["retrieved_content"])

    state["analyzed_content"] = analyzed_content

    return state
