"""Pulse in LangGraph — the same triage flow, built as an explicit graph.

Cross-framework re-implementation. In the Microsoft Agent Framework version, a
coordinator agent calls specialist agents as tools. Here, the same logic is a
LangGraph StateGraph: nodes are steps, edges are flow, and a conditional edge
routes negative feedback to a human-escalation step.
"""
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

DEPARTMENTS = {
    "product quality": "Product Management <product@company.com>",
    "delivery":        "Operations <ops@company.com>",
    "pricing":         "Finance <finance@company.com>",
    "support":         "Customer Support <support@company.com>",
    "freshness":       "Quality Assurance <qa@company.com>",
}


# --- State: the data that flows through the graph, filled in as it goes ---
class TriageState(TypedDict):
    feedback: str
    sentiment: str
    category: str
    department: str
    priority: str
    summary: str
    needs_review: bool


# --- Nodes: each reads the state and returns the fields it updates ---
def analyze(state: TriageState) -> dict:
    prompt = (
        "Analyze this customer feedback. Respond in EXACTLY this format, nothing else:\n"
        "Sentiment: <Positive|Neutral|Negative>\n"
        "Category: <Product Quality|Delivery|Pricing|Support|Freshness>\n\n"
        f"Feedback: {state['feedback']}"
    )
    text = llm.invoke(prompt).content
    sentiment, category = "Neutral", "Support"
    for line in text.splitlines():
        low = line.lower()
        if low.startswith("sentiment:"):
            sentiment = line.split(":", 1)[1].strip()
        elif low.startswith("category:"):
            category = line.split(":", 1)[1].strip()
    print(f"   [node: analyze]   -> {sentiment} | {category}")
    return {"sentiment": sentiment, "category": category}


def route(state: TriageState) -> dict:
    dept = DEPARTMENTS.get(state["category"].lower().strip(), "General Inquiries <hello@company.com>")
    print(f"   [node: route]     -> {dept}")
    return {"department": dept}


def escalate(state: TriageState) -> dict:
    print("   [node: escalate]  -> High priority, needs human review")
    return {"priority": "High", "needs_review": True}


def summarize(state: TriageState) -> dict:
    text = llm.invoke(f"Summarize this customer feedback in ONE short sentence: {state['feedback']}").content
    print("   [node: summarize] -> done")
    return {
        "summary": text.strip(),
        "priority": state.get("priority", "Low"),
        "needs_review": state.get("needs_review", False),
    }


# --- The conditional edge: decides the path based on sentiment ---
def route_by_sentiment(state: TriageState) -> str:
    return "escalate" if state["sentiment"].lower() == "negative" else "summarize"


# --- Build the graph: wire the nodes together with edges ---
def build_graph():
    builder = StateGraph(TriageState)
    builder.add_node("analyze", analyze)
    builder.add_node("route", route)
    builder.add_node("escalate", escalate)
    builder.add_node("summarize", summarize)

    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "route")
    builder.add_conditional_edges("route", route_by_sentiment,
                                  {"escalate": "escalate", "summarize": "summarize"})
    builder.add_edge("escalate", "summarize")
    builder.add_edge("summarize", END)

    return builder.compile()


SAMPLES = [
    "The tomatoes I got yesterday were mushy and clearly not fresh. Really disappointed.",
    "Delivery was super quick and the veggies were great!",
    "Why did onion prices jump 30% this week? Feels unfair.",
]


def main():
    graph = build_graph()
    for feedback in SAMPLES:
        print(f"\n=== Feedback: {feedback!r}")
        result = graph.invoke({"feedback": feedback})
        review = "   [NEEDS HUMAN REVIEW]" if result["needs_review"] else ""
        print(f"   [{result['priority']}] {result['sentiment']}  |  {result['category']}{review}")
        print(f"   -> {result['department']}")
        print(f"   Summary: {result['summary']}")


if __name__ == "__main__":
    main()