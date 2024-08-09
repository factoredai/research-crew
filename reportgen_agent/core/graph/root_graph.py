from langgraph.graph import StateGraph, END
from reportgen_agent.core.state import ReportGenState
from reportgen_agent.nodes.query_processing import process_query
from reportgen_agent.nodes.web_search import perform_web_search_node
from reportgen_agent.nodes.content_retrieval import retrieve_content
# from reportgen_agent.nodes.information_filtering import filter_information
from reportgen_agent.nodes.content_analysis import analyze_content
from reportgen_agent.nodes.report_generation import generate_report
from reportgen_agent.nodes.source_citation import add_citations
from reportgen_agent.nodes.output_refinement import refine_output
from reportgen_agent.nodes.final_review import review_final_output


def create_graph() -> StateGraph:
    """Creates and returns the ReportGen workflow graph."""

    # Initialize the stateful graph with the ReportGenState
    graph = StateGraph(ReportGenState)

    # Add nodes to the graph
    graph.add_node("query_processing", process_query)
    graph.add_node("web_search", perform_web_search_node)
    graph.add_node("content_retrieval", retrieve_content)
    # graph.add_node("information_filtering", filter_information)
    graph.add_node("content_analysis", analyze_content)
    graph.add_node("report_generation", generate_report)
    graph.add_node("source_citation", add_citations)
    graph.add_node("output_refinement", refine_output)
    graph.add_node("final_review", review_final_output)

    # Define edges to connect the nodes in sequence
    graph.add_edge("query_processing", "web_search")
    graph.add_edge("web_search", "content_retrieval")
    # graph.add_edge("content_retrieval", "information_filtering")
    # graph.add_edge("information_filtering", "content_analysis")
    graph.add_edge("content_analysis", "report_generation")
    graph.add_edge("report_generation", "source_citation")
    graph.add_edge("source_citation", "output_refinement")
    graph.add_edge("output_refinement", "final_review")

    # Set the entry and exit points for the graph
    graph.set_entry_point("query_processing")
    graph.set_finish_point("final_review")


    # Return the fully constructed graph
    return graph
