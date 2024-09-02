from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.constants import Send

from reportgen_agent.config import settings
from reportgen_agent.core.state import OverallState, SummaryState
from reportgen_agent.utils.helper_functions import retry_with_exponential_backoff

llm = ChatOpenAI(
    model=settings.pre_report_summarization.map_model,
    api_key=settings.general.openai_api_key,
)

map_prompt = ChatPromptTemplate.from_template(settings.pre_report_summarization.map_prompt)

map_chain = map_prompt | llm | StrOutputParser()


def map_summaries(state: OverallState):
    messages = [
        Send("generate_summary", {"content": content, "user_query": state["user_query"]})
        for content in state["analyzed_content"]
    ]
    return messages


def generate_summary(state: SummaryState, run_dir: str):
    # Log the prompt being sent to the LLM
    # formatted_prompt = map_prompt.format(content=state["content"], user_query=state["user_query"])
    # print(f"Sending prompt to LLM:\n{formatted_prompt}")

    response = retry_with_exponential_backoff(
        map_chain.invoke, input={"content": state["content"], "user_query": state["user_query"]}
    )

    # Log the response from the LLM
    # print(f"Received response from LLM:\n{response}")

    return {"summaries": [response]}


# Here we generate a summary, given a document
# async def generate_summary(state: SummaryState):
#     response = await map_chain.ainvoke(input=state["content"])
#     return {"summaries": [response]}
