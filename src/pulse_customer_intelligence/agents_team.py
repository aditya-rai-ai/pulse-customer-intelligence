from agent_framework import Agent
from src.pulse_customer_intelligence.config import get_chat_client
from src.pulse_customer_intelligence.tools import lookup_department
from src.pulse_customer_intelligence.knowledge import search_knowledge
from src.pulse_customer_intelligence.tracing import trace_middleware


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
        middleware=[trace_middleware],
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
        middleware=[trace_middleware],
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
        middleware=[trace_middleware],
    )


def build_advisor() -> Agent:
    """Uses the RAG knowledge base to draft a policy-grounded reply."""
    return Agent(
        client=get_chat_client(),
        name="advisor",
        description="Finds the relevant company policy and drafts a short, grounded reply to the customer.",
        instructions=(
            "You draft a short reply to a customer's feedback. "
            "First, call the search_knowledge tool to find the most relevant company policy. "
            "Then write ONE short, helpful sentence to the customer, grounded ONLY in what that "
            "policy says. Never invent a policy. Return only the sentence."
        ),
        tools=search_knowledge,
        middleware=[trace_middleware],
    )


def build_coordinator() -> Agent:
    """The parent agent. It calls the specialists (as tools) and assembles the result."""
    analyzer = build_analyzer()
    router = build_router()
    summarizer = build_summarizer()
    advisor = build_advisor()

    return Agent(
        client=get_chat_client(),
        name="coordinator",
        instructions=(
            "You coordinate a customer-feedback triage using your tools.\n"
            "Steps for each piece of feedback:\n"
            "1. Call the 'analyzer' tool to get sentiment and category.\n"
            "2. Call the 'router' tool with that category to get the owning department.\n"
            "3. Call the 'summarizer' tool to get a one-line summary.\n"
            "4. Call the 'advisor' tool to get a short, policy-grounded reply for the customer.\n"
            "5. Set priority: High if sentiment is Negative, otherwise Low.\n"
            "Then return ONLY a JSON object with keys: "
            "sentiment, category, owning_department, priority, summary, suggested_response. "
            "No text before or after the JSON."
        ),
        tools=[
            analyzer.as_tool(),
            router.as_tool(),
            summarizer.as_tool(),
            advisor.as_tool(),
        ],
        middleware=[trace_middleware],
    )