from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from reportgen_agent.config import settings
from reportgen_agent.core.state import OverallState

# TODO: This is been done twice, here and on `collapse_summaries.py`
llm = ChatOpenAI(
    model=settings.pre_report_summarization.reduce_model,
    api_key=settings.general.openai_api_key,
)
reduce_prompt = ChatPromptTemplate.from_template(settings.pre_report_summarization.reduce_prompt)
reduce_chain = reduce_prompt | llm | StrOutputParser()


def generate_final_summary(state: OverallState, run_dir: str):
    # Log the prompt being sent to the LLM
    # formatted_prompt = reduce_prompt.format(docs=state["collapsed_summaries"], user_query=state["user_query"])
    # print(f"Sending prompt to LLM:\n{formatted_prompt}")

    response = reduce_chain.invoke({"docs": state["collapsed_summaries"], "user_query": state["user_query"]})

    # Log the response from the LLM
    # print(f"Received response from LLM:\n{response}")

    return {"final_summary": response}


# Here we will generate the final summary
# async def generate_final_summary(state: OverallState):
#     response = await reduce_chain.ainvoke(
#         {"docs": state["collapsed_summaries"], "user_query": state["user_query"]}
#     )
#     return {"final_summary": response}
