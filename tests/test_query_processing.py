import os
import sys

# Add the parent directory to the Python path to import your module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportgen_agent.core.state import ReportGenState
from reportgen_agent.nodes.query_processing import (
    expand_concepts_with_llm,
    extract_keywords_with_llm,
    process_query,
)


def test_extract_keywords(query: str, max_keywords: int = 5):
    print(f"\nTesting keyword extraction for: '{query}'")
    keywords = extract_keywords_with_llm(query=query, max_keywords=max_keywords)
    print(f"Extracted keywords: {keywords}")
    return keywords


def test_expand_concepts(query: str, keywords: list, max_concepts: int = 5):
    print(f"\nTesting concept expansion for query: '{query}' and keywords: {keywords}")
    concepts = expand_concepts_with_llm(query=query, keywords=keywords, max_concepts=max_concepts)
    print(f"Expanded concepts: {concepts}")
    return concepts


def test_process_query(query: str):
    print(f"\nTesting full query processing for: '{query}'")
    state = ReportGenState(query=query)
    updated_state = process_query(state=state, run_dir="test_run")
    print(f"Updated state: {updated_state}")
    return updated_state


def run_tests():
    # Test cases
    test_queries = [
        "What are the latest advancements in renewable energy?",
        "Explain the impact of artificial intelligence on healthcare",
        "How does climate change affect biodiversity?",
        "What are the benefits and risks of genetic engineering in agriculture?",
        "Discuss the future of space exploration and potential Mars colonization",
    ]

    for query in test_queries:
        # Test keyword extraction
        keywords = test_extract_keywords(query)

        # Test concept expansion
        test_expand_concepts(query, keywords)

        # Test full query processing
        test_process_query(query)

        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    run_tests()
