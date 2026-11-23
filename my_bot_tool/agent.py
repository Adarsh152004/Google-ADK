from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search

root_agent = Agent(
    model="gemini-2.5-flash",
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that provides the current time in a specified city. Use the 'get_current_time' tool to fetch the time.",
    tools=[google_search],
)