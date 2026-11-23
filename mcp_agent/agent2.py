from google.adk.agents.llm_agent import Agent
from pathlib import Path

from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)


root_agent = Agent(
    model="gemini-3.5-flash",
    name="filesystem_agent",

    instruction=f"""
    Help users manage files in {folder}.

    Rules:
    - Use absolute paths only.
    - Never use relative paths.
    - Never access files outside {folder}.
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
        )
    ],
)