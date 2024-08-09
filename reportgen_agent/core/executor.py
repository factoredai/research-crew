from reportgen_agent.core.graph import create_graph
from reportgen_agent.core.state import ReportGenState

class ReportGenExecutor:
    """Executor class for managing the ReportGen workflow."""

    def __init__(self, query: str):
        """Initialize the executor with a query and create the graph."""
        self.query = query
        self.graph = create_graph()
        self.state = self._initialize_state()

    def _initialize_state(self) -> ReportGenState:
        """Initialize the workflow state with the query."""
        return ReportGenState(
            query=self.query,
            keywords=[],
            expanded_concepts=[],
            search_results=[],
            retrieved_content=[],
            filtered_content=[],
            analyzed_content=[],
            markdown_report=""
        )

    def run(self) -> str:
        """Run the workflow and return the final report."""
        result_state = self.graph.invoke(self.state)
        return result_state["markdown_report"]

# Example of how this class could be used:
# executor = ReportGenExecutor("How does Python handle multithreading in data pipelines?")
# final_report = executor.run()
# print(final_report)
