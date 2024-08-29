from reportgen_agent.core.state import ReportGenState
from reportgen_agent.utils import is_valid_url
from reportgen_agent.utils.web_fetcher import process_urls


# TODO: Improve to also retrieve from local files and pdfs
# What happen to URL of pdfs???
def retrieve_content(state: ReportGenState, run_dir: str) -> ReportGenState:
    """Retrieve content from the top search results and update the state.

    Parameters
    ----------
    state : ReportGenState
        The current state of the workflow.
    run_dir : str
        The directory path where the run-specific data is stored.

    Returns
    -------
    ReportGenState
        The updated state with the retrieved content.

    Notes
    -----
    This function processes the search results in the state, retrieves content
    from valid URLs, and updates the state with the retrieved content. The
    updated state is then saved to the specified run directory.
    """
    valid_urls = []
    for search_result in state["search_results"]:
        if is_valid_url(search_result["url"]):
            valid_urls.append(search_result["url"])

    retrieved_content = process_urls(valid_urls, run_dir)

    state["retrieved_content"] = retrieved_content

    return state
