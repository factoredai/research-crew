from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.constants import Send

from reportgen_agent.core.state import SummaryState
from reportgen_agent.core.state import OverallState
from reportgen_agent.config import settings


llm = ChatOpenAI(
    model=settings.pre_report_summarization.map_model, 
    api_key=settings.general.openai_api_key)

map_prompt = ChatPromptTemplate.from_messages(
    [("system", settings.pre_report_summarization.map_prompt)]
)

map_chain = map_prompt | llm | StrOutputParser()

def map_summaries(state: OverallState):
    messages = [
        Send("generate_summary", {"content": content}) 
        for content in state["analyzed_content"]
    ]
    return messages


def generate_summary(state: SummaryState, run_dir: str):
    response = map_chain.invoke(input=state["content"])
    return {"summaries": [response]}


# Here we generate a summary, given a document
# async def generate_summary(state: SummaryState):
#     response = await map_chain.ainvoke(input=state["content"])
#     return {"summaries": [response]}
