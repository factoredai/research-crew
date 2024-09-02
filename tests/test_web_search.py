import os
import sys
import traceback
from typing import List

# Add the parent directory to the Python path to import your module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from reportgen_agent.config import settings
    from reportgen_agent.core.state import ReportGenState
    from reportgen_agent.nodes.web_search import (
        get_search_provider,
        perform_web_search_node,
    )
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure that your project structure is correct and all required packages are installed.")
    sys.exit(1)


def check_api_keys() -> List[str]:
    """Check which API keys are defined and return a list of available providers."""
    api_key_mapping = {
        "serpapi": "serpapi_api_key",
        "google": "google_api_key",
        "bing": "bing_subscription_key",
        "brave": "brave_api_key",
        # "tavily": "tavily_api_key"
    }

    available_providers = []

    for provider, key_name in api_key_mapping.items():
        if getattr(settings.web_search, key_name, None):
            available_providers.append(provider)
        else:
            print(f"{key_name.upper()} is not set in settings. {provider.capitalize()} search will not be tested.")

    return available_providers


def test_web_search_node():
    """Test the web search node functionality."""
    print("\nTesting Web Search Node")
    print("=" * 40)

    state = ReportGenState(
        query="Latest advancements in AI",
        keywords=["AI", "advancements", "technology"],
        expanded_concepts=["machine learning", "neural networks", "deep learning"],
    )

    try:
        provider = get_search_provider()
        print(f"Current search provider: {provider.__class__.__name__}")

        updated_state = perform_web_search_node(state, run_dir="tests")

        print(f"Search Query: {updated_state['search_query']}")
        print(f"Number of search results: {len(updated_state['search_results'])}")

        for i, doc in enumerate(updated_state["search_results"][:3], 1):
            print(f"\nResult {i}:")
            print(f"Title: {doc.metadata['title']}")
            print(f"Source: {doc.metadata['source']}")
            print(f"Snippet: {doc.page_content[:100]}...")

    # all tracebacks will be printed here
    except Exception as e:
        print(f"Error in test_web_search_node: {str(e)}")
        print(traceback.format_exc())


def test_individual_providers(available_providers: List[str]):
    """Test each available search provider individually."""
    print("\nTesting Individual Search Providers")
    print("=" * 40)

    query = "What are the latest developments in quantum computing?"

    for provider_name in available_providers:
        print(f"\nTesting {provider_name.capitalize()} Search Provider")
        print("-" * 40)

        original_provider = settings.web_search.provider
        settings.web_search.provider = provider_name

        try:
            provider = get_search_provider()
            results = provider.search(query, settings.web_search.num_results)

            print(f"Number of results: {len(results)}")
            for i, result in enumerate(results[:3], 1):
                print(f"\nResult {i}:")
                print(f"Title: {result['title']}")
                print(f"URL: {result['link']}")
                print(f"Snippet: {result['snippet'][:100]}...")

        except Exception as e:
            print(f"Error testing {provider_name}: {str(e)}")
            print(traceback.format_exc())

        finally:
            settings.web_search.provider = original_provider


def run_tests():
    """Run all tests."""
    available_providers = check_api_keys()
    if not available_providers:
        print("No search providers available. Please set at least one API key in the settings.")
        return

    print(f"Available search providers: {', '.join(available_providers)}")

    test_web_search_node()
    test_individual_providers(available_providers)


if __name__ == "__main__":
    run_tests()
