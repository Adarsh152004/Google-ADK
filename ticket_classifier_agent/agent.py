from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field
from typing import Literal

class Ticket(BaseModel):
    category: Literal['refund', 'technical', 'course_query', 'payment', 'other'] = Field(
        description="The main topic of the student's message"
    )
    urgency: Literal['low', 'medium', 'high'] = Field(
        description="high = needs immediate attention, medium = can wait a day or two, low = can wait a week"
    )
    needs_human: bool = Field(
        description="True if a human must handle this: money disputes, anger or anything unclear."
    )

root_agent = Agent(
    name="ticket_classifier",
    model="gemini-3.5-flash",
    description="Classifies CampusX support messages into tickets.",
    instruction="""You classify support messages sent by CampusX students.
Read the message and fill in the ticket.
Be conservative: if money, anger or confusion is involved, set needs_human to true.""",
    output_schema=Ticket,
    output_key="ticket",
)