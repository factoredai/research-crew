import asyncio
import re
from typing import Any, Dict, List, Optional

import aiohttp
import html2text
from bs4 import BeautifulSoup

from reportgen_agent.utils.storage_utils import save_webpage


def process_urls(urls: List[str], run_dir: str) -> List[Optional[str]]:
    """Process a list of URLs asynchronously.

    Parameters
    ----------
    urls : List[str]
        List of URLs to process.
    run_dir : str
        Directory to save processed data.

    Returns
    -------
    List[Optional[str]]
        List of processed contents or None for failed URLs.
    """
    return asyncio.run(process_urls_async(urls=urls, run_dir=run_dir))


async def process_urls_async(**params: Dict[str, Any]) -> List[Optional[str]]:
    """Asynchronously process multiple URLs.


    Parameters
    ----------
    **params : Dict[str, Any]
        Dictionary containing 'urls' and 'run_dir'.

    Returns
    -------
    List[Optional[str]]
        List of processed contents or None for failed URLs.
    """
    urls = params["urls"]
    run_dir = params["run_dir"]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_save_url(session, url, run_dir) for url in urls]
        results = await asyncio.gather(*tasks)

    return results


# TODO: This is a naive way to scrape and avoid bot blocking. We will
# possibly need in the future more advanced techniques for bot passing
# and dealing with javascript-heavy sites (playwright or selenium for
# the rescue?)
async def fetch_and_save_url(session: aiohttp.ClientSession, url: str, run_dir: str) -> Optional[str]:
    """Fetch URL content, save it, and process it.

    Parameters
    ----------
    session : aiohttp.ClientSession
        Aiohttp session for making requests.
    url : str
        URL to fetch and process.
    run_dir : str
        Directory to save processed data.

    Returns
    -------
    Optional[str]
        Processed markdown content or None if failed.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
    }

    try:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: Status {response.status}")
                return None
            response_text = await response.text(encoding="utf-8")

        soup = BeautifulSoup(response_text, "html.parser")
        html_content = soup.prettify()
        save_webpage(html_content, run_dir, url, "retrieve_content")

        # TODO: html2text hasn't been updated in 12 years, there might be better
        # options to generate markdown from html
        markdown_content = html2text.html2text(html_content)
        markdown_content = remove_urls(markdown_content)
        markdown_content = remove_consecutive_empty_lines(markdown_content)
        markdown_content = remove_lines_with_special_chars_and_numbers(markdown_content)

        return markdown_content

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return None


# TODO: This reduce number of tokens but in the future we shouldn't do
# that as links on webpages might be good links to scrape data too.
def remove_urls(markdown_content: str) -> str:
    """Remove URLs and images from markdown content.

    Parameters
    ----------
    markdown_content : str
        Original markdown content.

    Returns
    -------
    str
        Markdown content with URLs and images removed.
    """
    markdown_content_no_images = re.sub(r"!\[.*?\]\([^)]+\)", "", markdown_content, flags=re.DOTALL)
    markdown_content_no_urls = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", markdown_content_no_images, flags=re.DOTALL)
    return markdown_content_no_urls


def remove_consecutive_empty_lines(markdown_content: str) -> str:
    """Remove consecutive empty lines from markdown content.

    Parameters
    ----------
    markdown_content : str
        Original markdown content.

    Returns
    -------
    str
        Markdown content with consecutive empty lines removed.
    """
    return re.sub(r"\n\s*\n+", "\n\n", markdown_content)


def remove_lines_with_special_chars_and_numbers(text: str) -> str:
    """Remove lines containing only special characters or numbers.

    Parameters
    ----------
    text : str
        Original text content.

    Returns
    -------
    str
        Text with lines containing only special characters or numbers removed.
    """
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        # Check if the line contains only special characters or numbers
        if (not re.match(r"^[^\w\s]*$", line)) and (not re.match(r"^\d*$", line)):
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text
