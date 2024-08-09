from typing import List, TypedDict

class ReportGenState(TypedDict):
    """Represents the state of the ReportGen workflow."""

    # The initial query provided by the user
    query: str

    # Extracted keywords from the query
    keywords: List[str]

    # Expanded concepts related to the query
    expanded_concepts: List[str]

    # Results from the web search (e.g., URLs, titles)
    search_results: List[str]

    # Full content retrieved from the top search results
    retrieved_content: List[str]

    # Analyzed and summarized content
    analyzed_content: List[str]

    # The final generated report in Markdown format
    markdown_report: str

    final_review_passed: bool
