from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor


def get_current_time(timezone: str) -> dict:
    """Get the current date and time in an IANA time zone.

    Args:
        timezone: IANA timezone such as "Asia/Kolkata",
                  "America/New_York", or "Europe/London".
    """

    try:
        now = datetime.now(ZoneInfo(timezone))

    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "error_message": (
                f"Unknown timezone '{timezone}'. "
                "Use a complete IANA timezone such as "
                "'Europe/London', 'Asia/Kolkata', or 'America/New_York'."
            ),
        }

    return {
        "status": "success",
        "timezone": timezone,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "weekday": now.strftime("%A"),
    }


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",

    description=(
        "A helpful assistant that can search the web, run Python code "
        "and tell the time anywhere."
    ),

    instruction=(
        "Answer user questions accurately.\n"

        "- Use Google Search for current information.\n"

        "- Use get_current_time whenever the user asks for the "
        "current time or date somewhere. Never guess the time.\n"

        "- Convert locations into complete IANA timezones before "
        "calling get_current_time.\n"

        "Examples:\n"
        "Mumbai -> Asia/Kolkata\n"
        "Delhi -> Asia/Kolkata\n"
        "London -> Europe/London\n"
        "Paris -> Europe/Paris\n"
        "New York -> America/New_York\n"
        "Tokyo -> Asia/Tokyo\n"

        "Never pass incomplete values such as 'Europe', 'Asia', "
        "or 'America' to get_current_time.\n"

        "- Write and run Python code for calculations or data analysis."
    ),

    tools=[
        google_search,
        get_current_time,
    ],

    code_executor=BuiltInCodeExecutor(),
)