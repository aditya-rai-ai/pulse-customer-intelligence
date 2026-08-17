from agent_framework import Agent
from src.pulse_customer_intelligence.config import get_chat_client
from src.pulse_customer_intelligence.tools import lookup_department


def build_analyzer() -> Agent:
    return Agent(
        client=get_chat_client(),
        name="analyzer",
        description="Reads customer feedback and determines its sentiment and category.",
        instructions=(
            "You analyze a single piece of customer feedback. "
            "Return sentiment (Positive, Neutral, or Negative) and ONE category "
            "(Product Quality, Delivery, Pricing, Support, or Freshness). "
            "Reply in the form: 'Sentiment: X | Category: Y'. Nothing else."
        ),
    )


def build_router() -> Agent:
    return Agent(
        client=get_chat_client(),
        name="router",
        description="Given a category, finds the owning department using the lookup tool.",
        instructions=(
            "You are given a feedback category. Call the lookup_department tool with that "
            "category and return exactly what the tool gives back. Nothing else."
        ),
        tools=lookup_department,
    )


def build_summarizer() -> Agent:
    return Agent(
        client=get_chat_client(),
        name="summarizer",
        description="Writes a one-sentence summary of a piece of customer feedback.",
        instructions=(
            "Summarize the given customer feedback in ONE short, factual sentence. "
            "Return only the sentence."
        ),
    )


def build_coordinator() -> Agent:
    """The parent agent. It calls the three specialists (as tools) and assembles the result."""
    analyzer = build_analyzer()
    router = build_router()
    summarizer = build_summarizer()

    return Agent(
        client=get_chat_client(),
        name="coordinator",
        instructions=(
            "You coordinate a customer-feedback triage using your tools.\n"
            "Steps for each piece of feedback:\n"
            "1. Call the 'analyzer' tool to get sentiment and category.\n"
            "2. Call the 'router' tool with that category to get the owning department.\n"
            "3. Call the 'summarizer' tool to get a one-line summary.\n"
            "4. Set priority: High if sentiment is Negative, otherwise Low.\n"
            "Then return ONLY a JSON object with keys: "
            "sentiment, category, owning_department, priority, summary. "
            "No text before or after the JSON."
        ),
        tools=[
            analyzer.as_tool(),
            router.as_tool(),
            summarizer.as_tool(),
        ],
    )