from typing import Dict

from reportgen_agent.core.state import ReportGenState


def check_relevance_to_query(report: str, user_query: str) -> bool:
    """
    Placeholder function to check if the report is relevant to the initial user_query.

    Args:
        report (str): The generated Markdown report.
        user_query (str): The initial user_query provided by the user.

    Returns:
        bool: True if the report is relevant, False otherwise.
    """
    # Placeholder implementation: Simple keyword check (this should be more complex in a real implementation)
    return user_query.lower() in report.lower()


def perform_final_review(state: ReportGenState) -> bool:
    """
    Perform a final review of the generated report to ensure it meets the requirements.

    Args:
        state (ReportGenState): The current state of the workflow.

    Returns:
        bool: True if the final review passes, False otherwise.
    """

    # Check if the report is relevant to the initial user_query
    is_relevant = check_relevance_to_query(state["markdown_report"], state["user_query"])

    # Additional checks can be implemented here, such as completeness, clarity, formatting, etc.

    return is_relevant


def review_final_output(state: ReportGenState) -> Dict:
    """
    Perform the final review of the report and update the state accordingly.

    Args:
        state (ReportGenState): The current state of the workflow.

    Returns:
        Dict: The updated state after the final review.
    """

    # Perform the final review
    review_passed = perform_final_review(state)

    # If the review does not pass, you might raise an error, or set a flag in the state.
    # For this placeholder, we'll just log the result.
    if not review_passed:
        print("Final review failed: The report may not be fully relevant to the user_query.")
        state["final_review_passed"] = False
    else:
        print("Final review passed: The report is ready for delivery.")
        state["final_review_passed"] = True

    # Here you could also update the state with a final review status if needed.

    # Return the state, unchanged or updated
    return state
