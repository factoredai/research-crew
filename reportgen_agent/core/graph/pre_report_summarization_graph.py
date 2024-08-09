from langgraph.graph import END, START, StateGraph

from reportgen_agent.utils import wrap_node_with_logging
from reportgen_agent.core.state import OverallState
from reportgen_agent.nodes.subnodes import (
    generate_summary,
    map_summaries, 
    collect_summaries, 
    collapse_summaries,
    should_collapse, 
    generate_final_summary,
)


# TODO: This graph should run asyncronously given the map-reduce nature.
# There is already some node async implementations commented but not sure
# how an async summarization subgraph would work in the may graph and 
# memory
def create_pre_report_summarization_graph(run_dir: str) -> StateGraph:
    graph = StateGraph(OverallState)
    graph.add_node("generate_summary", wrap_node_with_logging(generate_summary, run_dir))  # same as before
    graph.add_node("collect_summaries", wrap_node_with_logging(collect_summaries, run_dir))
    graph.add_node("collapse_summaries", wrap_node_with_logging(collapse_summaries, run_dir))
    graph.add_node("generate_final_summary", wrap_node_with_logging(generate_final_summary, run_dir))

    graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
    graph.add_edge("generate_summary", "collect_summaries")
    graph.add_conditional_edges("collect_summaries", should_collapse)
    graph.add_conditional_edges("collapse_summaries", should_collapse)
    graph.add_edge("generate_final_summary", END)

    return graph
