from reportgen_agent.core.graph import create_graph
from reportgen_agent.core.state import ReportGenState

def main():
    # Example input query
    query = "How does Python handle multithreading, and what are the best practices for using it in data pipelines?"

    # Initialize the state
    initial_state = ReportGenState(
        query=query,
        keywords=[],
        expanded_concepts=[],
        search_results=[],
        retrieved_content=[],
        filtered_content=[],
        analyzed_content=[],
        markdown_report=""
    )

    # Create the graph
    graph = create_graph()

    # Compile the graph into a runnable
    compiled_graph = graph.compile()

    # # Define the initial state
    # initial_state = {
    #     # Include your initial state data here
    # }

    # Execute the graph with the initial state
    result = compiled_graph.invoke(initial_state)

    # Print the final output (e.g., the generated Markdown report)
    print("Generated Report:")
    print(result["markdown_report"])

if __name__ == "__main__":
    main()

