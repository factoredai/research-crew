from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from reportgen_agent.config import settings
from reportgen_agent.core.state import ReportGenState

llm = ChatOpenAI(
    model=settings.report_generation.model,
    api_key=settings.general.openai_api_key,
)

prompt = ChatPromptTemplate.from_messages([("system", settings.report_generation.prompt.strip())])
report_generator_chain = prompt | llm | StrOutputParser()


def generate_markdown_report(content: str, user_query: str) -> str:
    """Generate a Markdown report from the analyzed content.

    Parameters
    ----------
    content : str
        The analyzed and summarized content.
    user_query : str
        The original query to be included in the report prompt.

    Returns
    -------
    str
        A structured Markdown report.

    Notes
    -----
    This function uses a language model chain to generate the report based on
    the provided content and user query.
    """
    report = report_generator_chain.invoke(
        input={
            "user_query": user_query,
            "content": content,
        }
    )
    return report


def generate_report(state: ReportGenState, run_dir: str) -> ReportGenState:
    """Generate a structured Markdown report and update the state.

    Parameters
    ----------
    state : ReportGenState
        The current state of the workflow.
    run_dir : str
        The directory where run-specific data is stored.

    Returns
    -------
    ReportGenState
        The updated state with the generated Markdown report.

    Notes
    -----
    This function extracts the analyzed content and query from the state,
    generates a Markdown report, and updates the state with the generated report.
    The analyzed_content is expected to be a single string, not a list.
    """

    markdown_report = generate_markdown_report(
        content=state["final_summary"],
        user_query=state["query"],
    )

    state["markdown_report"] = markdown_report

    return state
