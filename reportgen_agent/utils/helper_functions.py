import logging
import re
import sys
import time
import traceback
from typing import Callable, TypedDict
from urllib.parse import urlparse

from openai import RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .storage_utils import save_state

# Configure logging to output to the notebook cell
logging.basicConfig(
    level=logging.INFO,  # You can change this to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Direct logs to stdout
)


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RateLimitError),
)
def retry_with_exponential_backoff(func, *args, **kwargs):
    return func(*args, **kwargs)


# TODO: It doesn't seem right to wrap every node for adding logging and
# saving intermediate states. It would be better to have a single
# parent node class that encapsulate some common functionality.
def wrap_node_with_logging(
    node_func: Callable[[TypedDict, str], TypedDict], run_dir: str
) -> Callable[[TypedDict], TypedDict]:
    """Wrapper to log the start and end of each pipeline step and pass
    the run_dir to the node function.

    Parameters
    ----------
    node_func : Callable[[TypedDict, str], TypedDict]
        The original node function to be wrapped. It should accept a state (TypedDict) and
        a run_dir (str) as arguments, and return an updated state (TypedDict).
    run_dir : str
        The directory where run-specific data and logs are stored.

    Returns
    -------
    Callable[[TypedDict], TypedDict]
        A wrapped version of the node function that includes logging and error handling.

    Notes
    -----
    This wrapper adds the following functionality to the node function:
    1. Logs the start and end of each step.
    2. Measures and logs the duration of each step.
    3. Catches and logs any exceptions that occur during the step execution.
    4. Saves the state after successful execution of the step.
    """

    def wrapped_node_func(state: TypedDict) -> TypedDict:
        step_name = node_func.__name__
        logging.info(f"Starting step: {step_name}")
        start_time = time.time()
        try:
            result_state = node_func(state, run_dir)
            save_state(result_state, run_dir, step_name)

        except Exception as e:
            logging.error(f"Error in step {step_name}: {e}")
            logging.error(traceback.format_exc())
            raise
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Finished step: {step_name} (Time taken: {duration:.2f} seconds)")
        return result_state

    return wrapped_node_func


def is_valid_url(url: str) -> bool:
    """
    Check if a given URL is valid.

    Parameters
    ----------
    url : str
        The URL to be validated.

    Returns
    -------
    bool
        True if the URL is valid, False otherwise.

    Notes
    -----
    A URL is considered valid if it has both a scheme (e.g., http, https)
    and a network location (domain).

    Examples
    --------
    >>> is_valid_url("https://www.example.com")
    True
    >>> is_valid_url("invalid-url")
    False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def clean_text(text: str) -> str:
    """
    Clean up text by removing unwanted characters, extra spaces, etc.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.strip()


def setup_logging(log_level=logging.INFO) -> None:
    """
    Setup logging configuration.

    Args:
        log_level: The logging level (default: logging.INFO).
    """
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.info("Logging is set up.")


def chunk_text(text: str, chunk_size: int) -> list:
    """
    Split a long string into smaller chunks of a specified size.

    Args:
        text (str): The text to chunk.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of text chunks.
    """
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def extract_links(text: str) -> list:
    """
    Extract all URLs from a given text.

    Args:
        text (str): The text from which to extract URLs.

    Returns:
        list: A list of URLs found in the text.
    """
    return re.findall(r"http[s]?://\S+", text)


def validate_markdown_syntax(markdown_text: str) -> bool:
    """
    Placeholder function to validate the syntax of a Markdown document.

    Args:
        markdown_text (str): The Markdown text to validate.

    Returns:
        bool: True if the syntax is valid, False otherwise.
    """
    # Placeholder: Assume syntax is always valid
    return True
