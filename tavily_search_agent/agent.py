from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch


# 1. Create Tavily search tool
tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)

# 2. Wrap Tavily tool for ADK
tavily_tool = LangchainTool(
    tool=tavily_search,
    name="tavily_search",
    description="Search the web for current information.",
)

# 3. Create ADK agent
root_agent = Agent(
    name="root_agent",
    model=LiteLlm(
        model="openai/gpt-oss-120b",
    ),
    description="A helpful assistant that can search the web.",
    instruction="""
    Answer user questions accurately.

    Use the Tavily search tool when:
    - the user asks about current information,
    - you need to verify facts,
    - or your knowledge may be outdated.
    """,
    tools=[tavily_tool],
)


# import os
# import requests

# from google.adk.agents import Agent
# from google.adk.models.lite_llm import LiteLlm


# def tavily_search(query: str) -> str:
#     """Search the web using Tavily and return the results."""

#     response = requests.post(
#         "https://api.tavily.com/search",
#         json={
#             "api_key": os.getenv("TAVILY_API_KEY"),
#             "query": query,
#             "max_results": 5,
#             "topic": "general",
#         },
#     )

#     response.raise_for_status()

#     data = response.json()

#     return "\n\n".join(
#         f"Title: {result['title']}\n"
#         f"URL: {result['url']}\n"
#         f"Content: {result['content']}"
#         for result in data.get("results", [])
#     )


# root_agent = Agent(
#     name="root_agent",
#     model=LiteLlm(
#         model="openai/gpt-oss-120b",
#     ),
#     description="A helpful assistant that can search the web.",
#     instruction="""
#     Answer user questions accurately.

#     Use tavily_search whenever the question requires
#     current information or web verification.
#     """,
#     tools=[tavily_search],
# )