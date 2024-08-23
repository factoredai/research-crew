import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from reportgen_agent.core.state import OverallState
from reportgen_agent.config import settings

# TODO: This is been done twice, here and on `collapse_summaries.py`
llm = ChatOpenAI(
    model=settings.pre_report_summarization.reduce_model, 
    api_key= settings.general.openai_api_key,
)
reduce_prompt = ChatPromptTemplate(
    [("human", settings.pre_report_summarization.reduce_prompt)]
)
reduce_chain = reduce_prompt | llm | StrOutputParser()


def generate_final_summary(state: OverallState, run_dir: str):
    response = reduce_chain.invoke(state["collapsed_summaries"])
    return {"final_summary": response}


# Here we will generate the final summary
# async def generate_final_summary(state: OverallState):
#     response = await reduce_chain.ainvoke(state["collapsed_summaries"])
#     return {"final_summary": response}
