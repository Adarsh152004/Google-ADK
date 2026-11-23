from google.adk.agents.llm_agent import Agent
from pathlib import Path
import os

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from mcp import StdioServerParameters

from dotenv import load_dotenv
load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN is not set in the environment variables.")

folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)


root_agent = Agent(
    model="gemini-3.5-flash",
    name="github_agent",

    instruction=f"""
    You have access to a GitHub token. Use it to help users manage their GitHub repositories.
    Use their tools to manage local files and handle github workflow. 
    Local files are located in {folder}. Use absolute paths only. Never use relative paths. Never access files outside {folder}.
    """,

    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="cmd",
                    args=[
                        "/c",
                        "npx",
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        str(folder),
                    ],
                )
            )
        ),

        # GitHub toolset
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {github_token}",
                }
            )
        )
    ],
)

