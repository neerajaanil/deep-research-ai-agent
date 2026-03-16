"""Planner agent for creating research search plans."""

from pydantic import BaseModel, Field
from agents import Agent

from ..config import Config

INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {Config.HOW_MANY_SEARCHES} terms to query for."
)


class WebSearchItem(BaseModel):
    """Individual web search item."""
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    """Plan containing multiple web searches."""
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=Config.OPENAI_MODEL,
    output_type=WebSearchPlan,
)
