from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import yaml
# from dotenv import load_dotenv
import os
# load_dotenv(override=True)
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    SerperDevTool
)
from tools.bulk_scrapper import *

groq_llm = ChatGroq(temperature = 0, model_name="llama3-70b-8192")
gpt4o = ChatOpenAI(temperature = 0, model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
gpt35 = ChatOpenAI(temperature = 0, model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Function to load YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
agents_config = load_yaml('config/agents.yaml')
tasks_config = load_yaml('config/tasks.yaml')

# Agent tech_research_advisor
tra = agents_config.get('tech_research_advisor')
tech_research_advisor = Agent(
    role=tra.get('role'),
    goal=tra.get('goal'),
    backstory=tra.get('backstory'),
    verbose=tra.get('verbose'),
    allow_delegation=tra.get('allow_delegation'),
    human_input=tra.get('human_input'),
    llm = gpt4o
)

# Agent research_planner
rp = agents_config.get('research_planner')
research_planner = Agent(
    role = rp.get('role'),
    goal = rp.get('goal'),
    backstory = rp.get('backstory'),
    verbose = rp.get('verbose'),
    allow_delegation = rp.get('allow_delegation'),
    human_input = rp.get('human_input'),
    tools = [search_tool],
    llm = gpt4o
)

# Agent tech_research_analyst
tran = agents_config.get('tech_research_analyst')
tech_research_analyst = Agent(
    role = tran.get('role'),
    goal = tran.get('goal'),
    backstory = tran.get('backstory'),
    verbose = tran.get('verbose'),
    allow_delegation = tran.get('allow_delegation'),
    human_input = tran.get('human_input'),
    tools = [bulk_web_scraper],
    llm = gpt35,
    max_iter = 70,
    memory = True
)

# Agent tech_blog_writer
tbw = agents_config.get('tech_blog_writer')
tech_blog_writer = Agent(
    role = tbw.get('role'),
    goal = tbw.get('goal'),
    backstory = tbw.get('backstory'),
    verbose = tbw.get('verbose'),
    allow_delegation = tbw.get('allow_delegation'),
    human_input = tbw.get('human_input'),
    llm = gpt35,
)

# Task enhance_research_outline
ero = tasks_config.get('enhance_research_outline')
enhance_research_outline = Task(
    description = ero.get('description'),
    expected_output = ero.get('expected_output'),
    output_file = ero.get('output_file'),
    agent = tech_research_advisor,
    async_execution = False,
)

# Task plan_research
pr = tasks_config.get('plan_research')
plan_research = Task(
    description = pr.get('description'),
    expected_output = pr.get('expected_output'),
    output_file = pr.get('output_file'),
    agent = research_planner,
    async_execution = False,
)

# Task execute_research
sr = tasks_config.get('summarize_resources')
summarize_resources = Task(
    description = sr.get('description'),
    expected_output = sr.get('expected_output'),
    output_file = sr.get('output_file'),
    agent = tech_research_analyst,
    async_execution = False,
)

# Task write_blog
wb = tasks_config.get('write_blog')
write_blog = Task(
    description = wb.get('description'),
    expected_output = wb.get('expected_output'),
    output_file = wb.get('output_file'),
    agent = tech_blog_writer,
    async_execution = False,
    context = [enhance_research_outline, summarize_resources],
)

research_crew = Crew(
    agents=[tech_research_advisor,
            research_planner,
            tech_research_analyst,
            tech_blog_writer],
    tasks=[
        enhance_research_outline,
        plan_research,
        summarize_resources,
        write_blog
    ],
    verbose=True
)



## THIS SECTION DIDN'T WORK
# @CrewBase
# class ResearchCrew():
#     """An crewAI-based agentic workflow that takes a research topic and general research plan to then execute research and produce different types of content"""
#     agents_config = "config/agents.yaml"
#     tasks_config = "config/tasks.yaml"

#     def __init__(self) -> None:
#         self.groq_llm = ChatGroq(temperature = 0, model_name="llama3-70b-8192")
#         self.gpt4o = ChatOpenAI(temperature = 0, model="gpt-4o")
#         self.gpt35 = ChatOpenAI(temperature = 0, model="gpt-3.5-turbo")

#     ###### AGENTS START HERE ######
#     @agent
#     def tech_research_advisor(self) -> Agent:
#         return Agent(
#             config = self.agents_config['tech_research_advisor'], # on yaml
#             llm = self.gpt4o,
#         )
    
#     @agent
#     def research_planner(self) -> Agent:
#         return Agent(
#             config = self.agents_config['research_planner'], # on yaml
#             llm = self.gpt4o,
#         )
    
#     @agent
#     def tech_research_analyst(self) -> Agent:
#         return Agent(
#             config = self.agents_config['tech_research_analyst'], # on yaml
#             llm = self.groq_llm,
#         )
    
#     @agent
#     def tech_blog_writer(self) -> Agent:
#         return Agent(
#             config = self.agents_config['tech_blog_writer'], # on yaml
#             llm = self.gpt35,
#         )

#     ###### TASKS START HERE ######
#     @task
#     def enhance_research_outline(self) -> Task:
#         return Task(
#             config = self.tasks_config['enhance_research_outline'], # on yaml
#             agent = self.tech_research_advisor,
#         )
    
#     @task
#     def plan_research(self) -> Task:
#         return Task(
#             config = self.tasks_config['plan_research'], # on yaml
#             agent = self.research_planner,
#         )
    
#     @task
#     def execute_research(self) -> Task:
#         return Task(
#             config = self.tasks_config['execute_research'], # on yaml
#             agent = self.tech_research_analyst,
#         )
    
#     @task
#     def write_blog(self) -> Task:
#         return Task(
#             config = self.tasks_config['write_blog'], # on yaml
#             agent = self.tech_blog_writer,
#         )

#     ###### CREW DEFINED HERE ######
#     @crew
#     def crew(self) -> Crew:
#         return Crew(
#             agents = self.agents,
#             tasks = self.tasks,
#             process = Process.sequential,
#             verbose = 2,
#         )
    
