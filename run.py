import sqlite3
import os
import argparse
from typing import List

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from reportgen_agent.core.graph import create_pre_report_summarization_graph
from reportgen_agent.core.state import ReportGenState
from reportgen_agent.nodes.content_analysis import analyze_content
from reportgen_agent.nodes.content_retrieval import retrieve_content
from reportgen_agent.nodes.query_processing import process_query
from reportgen_agent.nodes.report_generation import generate_report
from reportgen_agent.nodes.web_search import perform_web_search_node
from reportgen_agent.utils import wrap_node_with_logging
from reportgen_agent.utils.storage_utils import create_run_directory


def main(query: str):
    """
    Main function to generate a report based on the given query.

    Parameters
    ----------
    query : str
        The user's query for report generation.

    Returns
    -------
    None
    """
    run_dir, run_id = create_run_directory()
    print(f"Run directory created at: {run_dir}")  # Log the run directory location

    initial_state = ReportGenState(
        query=query,
        keywords=[],
        expanded_concepts=[],
        search_results=[],
        retrieved_content=[],
        filtered_content=[],
        analyzed_content=[],
        markdown_report="",
    )

    graph = StateGraph(ReportGenState)
    pre_report_summarization_graph = create_pre_report_summarization_graph(run_dir + "/pre_report_summarization")

    ###########
    ## NODES ##
    ###########
    graph.add_node("query_processing", wrap_node_with_logging(process_query, run_dir))
    graph.add_node("web_search", wrap_node_with_logging(perform_web_search_node, run_dir))
    graph.add_node(
        "content_retrieval",
        wrap_node_with_logging(retrieve_content, run_dir),
    )
    graph.add_node("content_analysis", wrap_node_with_logging(analyze_content, run_dir))
    graph.add_node(
        "pre_report_summarization",
        pre_report_summarization_graph.compile(),
    )
    graph.add_node("report_generation", wrap_node_with_logging(generate_report, run_dir))

    ###########
    ## EDGES ##
    ###########
    graph.add_edge("query_processing", "web_search")
    graph.add_edge("web_search", "content_retrieval")
    graph.add_edge("content_retrieval", "content_analysis")
    graph.add_edge("content_analysis", "pre_report_summarization")
    graph.add_edge("pre_report_summarization", "report_generation")

    graph.set_entry_point("query_processing")
    graph.add_edge("report_generation", END)

    conn = sqlite3.connect("./data/checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)

    compiled_graph = graph.compile(checkpointer=memory)

    result = compiled_graph.invoke(
        initial_state,
        {"configurable": {"thread_id": "1"}},
    )

    print("Generated Report:")
    print(result["markdown_report"])

    # Save the markdown report to a file in the run directory
    report_file_path = os.path.join(run_dir, "generated_report.md")
    with open(report_file_path, "w") as f:
        f.write(result["markdown_report"])
    print(f"Report saved to: {report_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a report based on a user query.",
        epilog="Example usage: python run.py 'What are the latest AI trends?'"
    )
    parser.add_argument("query", type=str, help="The user's query for report generation.")
    args = parser.parse_args()

    main(query=args.query)
