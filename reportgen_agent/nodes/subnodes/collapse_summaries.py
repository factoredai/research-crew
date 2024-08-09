import os
from typing import List, Literal

from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    collapse_docs,
    split_list_of_docs,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph

from reportgen_agent.core.state import OverallState
from reportgen_agent.nodes.subnodes import (
    generate_summary, 
    collect_summaries, 
    collapse_summaries, 
    generate_final_summary
)
from reportgen_agent.config import settings

TOKEN_MAX = settings.pre_report_summarization.max_num_tokens2summarize

# TODO: This is been done twice, here and on `generate_final_summary.py`
llm = ChatOpenAI(
    model=settings.pre_report_summarization.reduce_model, 
    api_key=settings.general.openai_api_key,
)
reduce_prompt = ChatPromptTemplate(
    [("human", settings.pre_report_summarization.reduce_prompt)]
)
reduce_chain = reduce_prompt | llm | StrOutputParser()


def get_num_tokens(documents: List[Document]) -> int:
    """Get number of tokens for input contents."""
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)


def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = get_num_tokens(state["collapsed_summaries"])
    if num_tokens > TOKEN_MAX:
        return "collapse_summaries"
    else:
        return "generate_final_summary"


def collapse_summaries(state: OverallState, run_dir: str):
    doc_lists = split_list_of_docs(
        state["collapsed_summaries"], get_num_tokens, TOKEN_MAX
    )
    results = []
    for doc_list in doc_lists:
        results.append(collapse_docs(doc_list, reduce_chain.invoke))

    return {"collapsed_summaries": results}


# Add node to collapse summaries
# async def collapse_summaries(state: OverallState):
#     doc_lists = split_list_of_docs(
#         state["collapsed_summaries"], get_num_tokens, TOKEN_MAX
#     )
#     results = []
#     for doc_list in doc_lists:
#         results.append(await acollapse_docs(doc_list, reduce_chain.ainvoke))

#     return {"collapsed_summaries": results}
