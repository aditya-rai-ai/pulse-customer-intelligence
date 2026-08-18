"""Pulse's guardrails — safety checks around the agent.

Two kinds:
- Input guardrail: reject bad input before it reaches the agent.
- Output guardrail: flag risky or sensitive replies for a human to review.
"""

# Phrases a reply shouldn't make without a real, approved policy behind it.
RISKY_PHRASES = [
    "guarantee", "guaranteed", "compensation", "lawsuit", "sue",
    "legal action", "100% refund", "full refund", "unlimited",
]


def check_input(feedback: str) -> str | None:
    """Input guardrail. Returns an error message if the feedback is bad, else None."""
    text = feedback.strip()
    if not text:
        return "Empty feedback — nothing to process."
    if len(text) < 5:
        return "Feedback too short to be meaningful."
    return None


def check_output(reply: str, priority: str) -> list[str]:
    """Output guardrail. Returns a list of review flags (empty list = all clear)."""
    flags: list[str] = []
    lowered = reply.lower()
    for phrase in RISKY_PHRASES:
        if phrase in lowered:
            flags.append(f"Reply contains a risky promise: '{phrase}' — verify it's backed by policy.")
    if priority == "High":
        flags.append("High-priority (negative) feedback — a human should review before this reply is sent.")
    return flags