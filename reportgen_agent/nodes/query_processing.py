from typing import Dict, List

from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from reportgen_agent.config import settings
from reportgen_agent.core.state import ReportGenState
from reportgen_agent.utils.helper_functions import retry_with_exponential_backoff


class Keywords(BaseModel):
    """Schema for the extracted keywords."""

    keywords: List[str] = Field(description="List of important keywords extracted from the user_query")


class Concepts(BaseModel):
    """Schema for the expanded concepts."""

    concepts: List[str] = Field(description="List of expanded concepts related to the user_query")


def extract_keywords_with_llm(user_query: str, max_keywords: int = 5) -> List[str]:
    """
    Extract keywords from the user_query using LangChain's structured output
    feature.

    Parameters
    ----------
    user_query : str
        The original user user_query.
    max_keywords : int, optional
        Maximum number of keywords to extract, by default 5.

    Returns
    -------
    List[str]
        List of extracted keywords.
    """
    model = ChatOpenAI(
        model=settings.query_processing.keyword_extraction_model,
        api_key=settings.general.openai_api_key,
    )
    structured_llm = model.with_structured_output(Keywords)

    prompt = ChatPromptTemplate.from_template(settings.query_processing.keyword_extraction_prompt)

    response = retry_with_exponential_backoff(
        structured_llm.invoke, prompt.format(user_query=user_query, max_keywords=max_keywords)
    )

    return response.keywords


def expand_concepts_with_llm(user_query: str, keywords: List[str], max_concepts: int = 10) -> List[str]:
    """
    Expand concepts using LangChain's structured output feature with
    LLM.

    Parameters
    ----------
    user_query : str
        The original user user_query.
    keywords : List[str]
        List of keywords extracted from the user_query.
    max_concepts : int, optional
        Maximum number of expanded concepts to return, by default 10.

    Returns
    -------
    List[str]
        List of expanded concepts.
    """
    model = ChatOpenAI(
        model=settings.query_processing.concept_expansion_model,
        api_key=settings.general.openai_api_key,
    )
    structured_llm = model.with_structured_output(Concepts)

    prompt = ChatPromptTemplate.from_template(settings.query_processing.concept_expansion_prompt)

    response = retry_with_exponential_backoff(
        structured_llm.invoke,
        prompt.format(user_query=user_query, keywords=", ".join(keywords), max_concepts=max_concepts),
    )

    return list(set(response.concepts + keywords))


def process_query(state: ReportGenState, run_dir: str) -> Dict:
    """
    Process the input user_query by extracting keywords and expanding
    concepts using LLMs.

    Parameters
    ----------
    state : ReportGenState
        The current state of the workflow.
    run_dir : str
        The directory for the current run.

    Returns
    -------
    Dict
        The updated state with extracted keywords and expanded concepts.
    """
    user_query = state["user_query"]

    keywords = extract_keywords_with_llm(user_query=user_query, max_keywords=settings.query_processing.max_keywords)
    state["keywords"] = keywords

    if settings.query_processing.expand_concepts:
        expanded_concepts = expand_concepts_with_llm(
            user_query=user_query,
            keywords=keywords,
            max_concepts=settings.query_processing.max_concepts,
        )
        state["expanded_concepts"] = expanded_concepts

    return state
