
from langchain_core.documents import Document
from reportgen_agent.core.state import OverallState

def collect_summaries(state: OverallState, run_dir: str):
    return {
        "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
    }
