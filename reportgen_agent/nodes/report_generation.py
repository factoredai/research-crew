from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from reportgen_agent.config import settings
from reportgen_agent.core.state import ReportGenState
from reportgen_agent.utils.helper_functions import retry_with_exponential_backoff

llm = ChatOpenAI(
    model=settings.report_generation.model,
    api_key=settings.general.openai_api_key,
)

prompt = ChatPromptTemplate.from_template(settings.report_generation.prompt)
report_generator_chain = prompt | llm | StrOutputParser()


def generate_markdown_report(content: str, user_query: str) -> str:
    """Generate a Markdown report from the analyzed content.

    Parameters
    ----------
    content : str
        The analyzed and summarized content.
    user_query : str
        The original user_query to be included in the report prompt.

    Returns
    -------
    str
        A structured Markdown report.

    Notes
    -----
    This function uses a language model chain to generate the report based on
    the provided content and user user_query.
    """
    report = retry_with_exponential_backoff(
        report_generator_chain.invoke,
        {
            "user_query": user_query,
            "content": content,
        },
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
    This function extracts the analyzed content and user_query from the state,
    generates a Markdown report, and updates the state with the generated report.
    The analyzed_content is expected to be a single string, not a list.
    """

    markdown_report = generate_markdown_report(
        content=state["final_summary"],
        user_query=state["user_query"],
    )

    state["markdown_report"] = markdown_report

    return state
