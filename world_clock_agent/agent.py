from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents import Agent


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
    model="gemini-3.5-flash",
    name="clock_agent",
    description="Tells the current time and date anywhere in the world.",
    instruction="""
    You tell users the current time and date in any city or country.

    IMPORTANT:
    The get_current_time tool requires a COMPLETE IANA timezone.

    Always convert the user's location into an IANA timezone yourself.

    Examples:
    Mumbai -> Asia/Kolkata
    Delhi -> Asia/Kolkata
    London -> Europe/London
    Paris -> Europe/Paris
    Berlin -> Europe/Berlin
    New York -> America/New_York
    Tokyo -> Asia/Tokyo
    Singapore -> Asia/Singapore
    Dubai -> Asia/Dubai
    Sydney -> Australia/Sydney

    Never pass only a continent or region such as:
    "Europe", "Asia", "America", or "Australia".

    If the user asks for London, call:
    get_current_time(timezone="Europe/London")

    If the tool returns status="error", explain the error.
    """,
    tools=[get_current_time],
)