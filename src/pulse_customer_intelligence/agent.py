from agent_framework import Agent
from src.pulse_customer_intelligence.config import get_chat_client
from src.pulse_customer_intelligence.tools import lookup_department

INSTRUCTIONS = """You are a customer-feedback triage agent.
For each piece of customer feedback:
1. Decide the sentiment: Positive, Neutral, or Negative.
2. Classify it into ONE category: Product Quality, Delivery, Pricing, Support, or Freshness.
3. Use the lookup_department tool to find which team owns that category.
4. Set a priority: High for any Negative feedback, otherwise Medium or Low.
5. Give a short, clear result."""

def build_agent() -> Agent:
    return Agent(
        client=get_chat_client(),
        name="feedback-triage-agent",
        instructions=INSTRUCTIONS,
        tools=lookup_department,
    )