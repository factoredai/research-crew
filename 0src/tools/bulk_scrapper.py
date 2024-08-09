from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from typing import List, Any
import requests
from bs4 import BeautifulSoup

class SearchInput(BaseModel):
    websites: str = Field(description="a list of urls to scrape")

# @tool
def mytool_test(websites: str) -> str:
    "this function doesnt do anything"
    return websites

@tool
def bulk_web_scraper(websites: List[str]) -> str:
    """Scrape and summarize multiple websites"""
    # groq_llm = ChatGroq(temperature = 0, model_name="llama3-70b-8192") # wont fit context
    gpt35 = ChatOpenAI(temperature = 0, model="gpt-3.5-turbo")
    summaries = []
    for website in websites:
        print(f"Scrapping website: {website}")
        html_content = scrape_page(website_url=website)

        prompt_template = PromptTemplate.from_template(
            """Summarize the following html content scraped from a website: ```{html_content}```.
            Make sure to include at least the main 5 ideas and provide key details and support for each.```"""
        )
        prompt = prompt_template.format(html_content=html_content)
        messages = [
            SystemMessage(content="You take scraped information from websites and summarize concisely but including enough detail for further analysis"),
            HumanMessage(content=prompt),
        ]

        result = gpt35.invoke(messages)
        summaries.append(f"Summary for URL: {website} \n {result.content}")
        # print(result)
    return "\n".join(summaries)

def scrape_page(**kwargs: Any) -> str:
    website_url = kwargs.get('website_url')
    page = requests.get(
        website_url,
        timeout=15,
        headers= {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate, br'
        },
        #cookies=kwargs.get('cookies') if self.cookies else {}
    )
    parsed = BeautifulSoup(page.content, "html.parser")
    text = parsed.get_text()
    text = '\n'.join([i for i in text.split('\n') if i.strip() != ''])
    text = ' '.join([i for i in text.split(' ') if i.strip() != ''])
    return text